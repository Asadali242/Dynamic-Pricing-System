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
                    AVG(CASE WHEN EXTRACT(HOUR FROM oi.createdate) = %s THEN oi.store_item_price ELSE NULL END) AS months_average_price_this_hour,
                    AVG(oi.store_item_price) AS months_overall_average_price
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

    def fetchDataForSeasonRuleRecommendations(self):
        conn = self.db.connect()
        if conn is None:
            return {}

        try:
            cur = conn.cursor()

            # seasons based on months
            seasons = {
                "Winter": [12, 1, 2],
                "Spring": [3, 4, 5],
                "Summer": [6, 7, 8],
                "Fall": [9, 10, 11]
            }

            current_season = self.getCurrentSeason()

            #start and end dates for the previous year's seasons
            today = datetime.now()
            last_year_start = datetime(today.year - 1, 1, 1)
            last_year_end = datetime(today.year - 1, 12, 31)

            # Query to fetch data for each category
            query = """
                SELECT c.name AS category_name,
                    si.name AS item_name,
                    si.price AS current_price,
                    AVG(oi.quantity) AS overall_average_quantity_any_given_season,
                    AVG(CASE WHEN EXTRACT(MONTH FROM oi.createdate) IN %s THEN oi.quantity ELSE NULL END) AS average_quantity_current_season,
                    AVG(oi.store_item_price) AS overall_average_price_any_given_season,
                    AVG(CASE WHEN EXTRACT(MONTH FROM oi.createdate) IN %s THEN oi.store_item_price ELSE NULL END) AS average_price_this_season
                FROM storeitems si
                JOIN storeitemcategories sic ON si.id = sic.store_item_id
                JOIN categories c ON sic.category_id = c.id
                JOIN orderitems oi ON si.id = oi.store_item_id
                WHERE si.manual_seasonality_rule->>'active' = 'false'
                    AND oi.createdate BETWEEN %s AND %s
                GROUP BY c.name, si.name, si.price;
            """
            cur.execute(query, (tuple(seasons[current_season]), tuple(seasons[current_season]), last_year_start, last_year_end))
            data = cur.fetchall()

            # Construct the result dictionary
            result = {}
            for row in data:
                category_name = row[0]
                item_name = row[1]
                current_price = row[2]
                overall_average_quantity_any_given_season = row[3]
                average_quantity_current_season = row[4]
                overall_average_price_any_given_season = row[5]
                average_price_this_season = row[6]

                # Handle null values
                if current_price is None:
                    current_price = "N/A"
                if overall_average_quantity_any_given_season is None:
                    overall_average_quantity_any_given_season = "N/A"
                if average_quantity_current_season is None:
                    average_quantity_current_season = "N/A"
                if overall_average_price_any_given_season is None:
                    overall_average_price_any_given_season = "N/A"
                if average_price_this_season is None:
                    average_price_this_season = "N/A"
                    
                # Create a dictionary with descriptive variable names
                item_data = {
                    "name": item_name,
                    "currentPrice": current_price,
                    "overallAverageQuantityAnyGivenSeason": overall_average_quantity_any_given_season,
                    "averageQuantityCurrentSeason": average_quantity_current_season,
                    "overallAveragePriceAnyGivenSeason": overall_average_price_any_given_season,
                    "averagePriceThisSeason": average_price_this_season
                }

                # Add item data to the result dictionary
                if category_name not in result:
                    result[category_name] = {}
                result[category_name][item_name] = item_data

            return result

        except psycopg2.Error as e:
            print("Error fetching data for season rule recommendations:", e)
            return {}
        finally:
            self.db.close(conn, cur)

    def getCurrentSeason(self):
        seasons = {
            "Winter": [12, 1, 2],
            "Spring": [3, 4, 5],
            "Summer": [6, 7, 8],
            "Fall": [9, 10, 11]
        }
        current_month = datetime.now().month
        current_season = None
        for season, months in seasons.items():
            if current_month in months:
                current_season = season
                break

        return current_season
