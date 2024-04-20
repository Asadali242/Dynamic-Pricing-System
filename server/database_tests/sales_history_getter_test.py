import unittest
from database.sales_history_getter import SalesHistoryGetter
from database.database import Database
import psycopg2
from datetime import datetime, timedelta
import random
import uuid

class SalesHistoryGetterTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
        DB_PORT = 5432
        DB_USER = "lulapricingtest"
        DB_PASSWORD = "luladbtest"
        DB_NAME = "postgres"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.sales_history_getter = SalesHistoryGetter(self.db)

    def insert_sample_data(self, sample_data):
        conn = psycopg2.connect(
            dbname="postgres",
            user="lulapricingtest",
            password="luladbtest",
            host="lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com",
            port=5432
        )

        try:
            cur = conn.cursor()
            for data in sample_data:
                cur.execute(
                    """
                    INSERT INTO orderitems (id, store_item_id, quantity, store_item_price, store_item_total_price, createdate)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (data['id'], data['store_item_id'], data['quantity'], data['store_item_price'],
                    data['store_item_total_price'], data['createdate'])
                )
            conn.commit()
        except psycopg2.Error as e:
            print("Error inserting data:", e)
            conn.rollback()
        finally:
            conn.close()

    def generate_orderitem_sample_data(self, store_item_id, store_item_price):
        # Define start and end dates for the past 30 days
        end_date = datetime(2024, 5, 20)  # Today's date
        start_date = end_date - timedelta(days=70)

        # Initialize a list to store the sample data
        sample_data = []

        # Generate sample data for each day over the past 30 days
        current_date = start_date
        while current_date <= end_date:
            # Generate at least 24 data points per day, skewing towards 15:00
            for _ in range(random.randint(24, 30)):
                # Generate a random hour between 0 and 23, skewing towards 15:00
                hour = int(random.triangular(0, 23, 15))
                # Generate a random quantity between 1 and 5
                quantity = random.randint(1, 5)
                # Generate a store item total price
                # Randomize the store item price around the given price
                randomized_price = random.uniform(store_item_price - 2, store_item_price + 2)
                # Ensure the price is non-negative
                store_item_price = max(0, randomized_price)
                # Generate a store item total price
                store_item_total_price = quantity * store_item_price
                # Create a random datetime for the current data point
                createdate = datetime(current_date.year, current_date.month, current_date.day, hour)

                # Round the price to the nearest whole cent
                rounded_store_item_price = round(store_item_price)
                rounded_store_item_total_price = round(store_item_total_price)

                # Append the sample data point to the list
                sample_data.append({
                    'id': str(uuid.uuid4()),
                    'store_item_id': store_item_id,
                    'quantity': quantity,
                    'store_item_price': rounded_store_item_price,
                    'store_item_total_price': rounded_store_item_total_price,
                    'createdate': createdate
                })
            # Move to the next day
            current_date += timedelta(days=1)

        return sample_data

    # This case inserts a load of sample data into orderitems, given item id and price.
    # Careful because this is intensive on the database and we should be careful with the budget
    '''
    def test_insert_orderitem_sample_data(self):
        # Populate data up to May 20 and 70 days prior for testing
        # Sample data is for each 5 items within the 5 sample categories
        self.insert_sample_data(self.generate_orderitem_sample_data('10000000-0000-0000-0000-000000000000', 249))
        self.insert_sample_data(self.generate_orderitem_sample_data('20000000-0000-0000-0000-000000000000', 249))
        self.insert_sample_data(self.generate_orderitem_sample_data('30000000-0000-0000-0000-000000000000', 149))
        self.insert_sample_data(self.generate_orderitem_sample_data('40000000-0000-0000-0000-000000000000', 299))
        self.insert_sample_data(self.generate_orderitem_sample_data('50000000-0000-0000-0000-000000000000', 519))
        self.insert_sample_data(self.generate_orderitem_sample_data('60000000-0000-0000-0000-000000000000', 299))
        self.insert_sample_data(self.generate_orderitem_sample_data('70000000-0000-0000-0000-000000000000', 219))
        self.insert_sample_data(self.generate_orderitem_sample_data('80000000-0000-0000-0000-000000000000', 199))
        self.insert_sample_data(self.generate_orderitem_sample_data('90000000-0000-0000-0000-000000000000', 189))
        self.insert_sample_data(self.generate_orderitem_sample_data('11000000-0000-0000-0000-000000000000', 149))

        self.insert_sample_data(self.generate_orderitem_sample_data('12000000-0000-0000-0000-000000000000', 699))
        self.insert_sample_data(self.generate_orderitem_sample_data('13000000-0000-0000-0000-000000000000', 699))
        self.insert_sample_data(self.generate_orderitem_sample_data('14000000-0000-0000-0000-000000000000', 699))
        self.insert_sample_data(self.generate_orderitem_sample_data('15000000-0000-0000-0000-000000000000', 899))
        self.insert_sample_data(self.generate_orderitem_sample_data('16000000-0000-0000-0000-000000000000', 599))

        self.insert_sample_data(self.generate_orderitem_sample_data('17000000-0000-0000-0000-000000000000', 169))
        self.insert_sample_data(self.generate_orderitem_sample_data('18000000-0000-0000-0000-000000000000', 179))
        self.insert_sample_data(self.generate_orderitem_sample_data('19000000-0000-0000-0000-000000000000', 309))
        self.insert_sample_data(self.generate_orderitem_sample_data('21000000-0000-0000-0000-000000000000', 304))
        self.insert_sample_data(self.generate_orderitem_sample_data('22000000-0000-0000-0000-000000000000', 384))

        self.insert_sample_data(self.generate_orderitem_sample_data('23000000-0000-0000-0000-000000000000', 850))
        self.insert_sample_data(self.generate_orderitem_sample_data('24000000-0000-0000-0000-000000000000', 950))
        self.insert_sample_data(self.generate_orderitem_sample_data('25000000-0000-0000-0000-000000000000', 999))
        self.insert_sample_data(self.generate_orderitem_sample_data('26000000-0000-0000-0000-000000000000', 229))
        self.insert_sample_data(self.generate_orderitem_sample_data('27000000-0000-0000-0000-000000000000', 119))
    '''

    def test_fetch_data_for_time_rule_recommendations(self):
        print(self.sales_history_getter.fetchDataForTimeRuleRecommendations())


if __name__ == "__main__":
    unittest.main()