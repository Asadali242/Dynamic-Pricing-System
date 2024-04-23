from .database import Database
import psycopg2
from datetime import datetime, timedelta


class SalesHistoryGetter(Database):
    def __init__(self, db):
        self.db = db

    def fetchDataForTimeRuleRecommendations(self):
        conn = self.db.connect()
        if conn is None:
            return {}

        try:
            cur = conn.cursor()

            # Calculate the start and end date for the past month
            today = datetime.now()
            start_date = today - timedelta(days=31)

            # Query to fetch data for each category
            query = """
                SELECT c.name AS category_name,
                    si.name AS item_name,
                    si.price AS current_price,
                    AVG(CASE WHEN EXTRACT(HOUR FROM oi.createdate) = %s THEN oi.quantity ELSE 0 END) AS months_average_units_this_hour,
                    AVG(oi.quantity) AS months_overall_average_units_at_any_given_hour,
                    AVG(CASE WHEN EXTRACT(HOUR FROM oi.createdate) = %s THEN si.price ELSE NULL END) AS months_average_price_this_hour,
                    AVG(si.price) AS months_overall_average_price
                FROM storeitems si
                JOIN storeitemcategories sic ON si.id = sic.store_item_id
                JOIN categories c ON sic.category_id = c.id
                JOIN orderitems oi ON si.id = oi.store_item_id
                WHERE si.manual_time_rule->>'active' = 'false'
                    AND oi.createdate BETWEEN %s AND %s
                GROUP BY c.name, si.name, si.price;
            """
            cur.execute(query, (today.hour, today.hour, start_date, today - timedelta(days=1)))
            data = cur.fetchall()

            # Construct the result dictionary
            result = {}
            for row in data:
                category_name = row[0]
                item_name = row[1]
                current_price = row[2]
                months_average_quantity_current_hour = row[3]
                months_overall_average_quantity_any_given_hour = row[4]
                months_average_price_this_hour = row[5]
                months_overall_average_price_any_given_hour = row[6]

                # Handle null values
                if current_price is None:
                    current_price = "N/A"
                if months_average_quantity_current_hour is None:
                    months_average_quantity_current_hour = "N/A"
                if  months_overall_average_quantity_any_given_hour is None:
                    months_overall_average_quantity_any_given_hour = "N/A"
                if months_average_price_this_hour is None:
                    months_average_price_this_hour = "N/A"
                if months_overall_average_price_any_given_hour is None:
                    months_overall_average_price_any_given_hour = "N/A"
                    
                # Create a dictionary with descriptive variable names
                item_data = {
                    "name": item_name,
                    "currentPrice": current_price,
                    "monthsOverallAverageQuantityAnyGivenHour": months_overall_average_quantity_any_given_hour,
                    "monthsAverageQuantityCurrentHour": months_average_quantity_current_hour,
                    "monthsOverallAveragePriceAnyGivenHour": months_overall_average_price_any_given_hour,
                    "monthsAveragePriceThisHour": months_average_price_this_hour
                }

                # Add item data to the result dictionary
                if category_name not in result:
                    result[category_name] = {}
                result[category_name][item_name] = item_data

            return result

        except psycopg2.Error as e:
            print("Error fetching data for time rule recommendations:", e)
            return {}
        finally:
            self.db.close(conn, cur)
