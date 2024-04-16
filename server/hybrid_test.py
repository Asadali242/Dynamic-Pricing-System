import database
import json
import unittest
import psycopg2
from datetime import datetime, timedelta
import random
import uuid



def insert_sample_data(sample_data):
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

def generate_orderitem_sample_data(store_item_id, store_item_price):
    # Define start and end dates for the past 30 days
    end_date = datetime(2024, 4, 12)  # Today's date
    start_date = end_date - timedelta(days=29)

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

#this case inserts a load of sample data into orderitems, given item id and price.
#careful because this is intensive on the database and we should be careful with the budget
'''
class generateSampleData(unittest.TestCase):
    def test_insert_orderitem_sample_data(self):
        insert_sample_data(generate_orderitem_sample_data('10000000-0000-0000-0000-000000000000', 249))
'''

class TestDatabaseFunctions(unittest.TestCase):
    def test_fetch_data_for_time_rule_recommendations(self):
        print(database.fetchDataForTimeRuleRecommendations())


        
if __name__ == '__main__':
    unittest.main()