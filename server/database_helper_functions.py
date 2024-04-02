import json
from datetime import datetime
import psycopg2
from psycopg2 import Error
import datetime
import pytz
from decimal import Decimal

DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "lulapricingtest"
DB_PASSWORD = "luladbtest"
DB_NAME = "postgres"

def getCurrentHour(timezone):
    if timezone.upper() == 'EST':
        timezone = 'US/Eastern'
    if timezone.upper() == 'PST':
        timezone = 'US/Pacific'
    current_time = datetime.datetime.now(pytz.timezone(timezone))
    return current_time.hour

def fetchActiveManualHourRuleStoreItems():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cur = conn.cursor()
        query = """
            SELECT id, manual_time_rule
            FROM storeitems
            WHERE manual_time_rule->>'active' = 'true'
        """
        cur.execute(query)
        relevant_store_items = cur.fetchall()
        cur.close()
        conn.close()
        return relevant_store_items
    except Error as e:
        print("Error fetching active manual hour rule store items:", e)
        return []   

def fetchItemPriceFromDatabase(item_id):
    try:
        # Establish connection to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cur = conn.cursor()

        # Query to fetch item price by item_id
        query = """
            SELECT price
            FROM storeitems
            WHERE id = %s
        """
        cur.execute(query, (item_id,))
        price_in_cents = cur.fetchone()[0]  # Fetch the first column of the first row (price in cents)

        # Close cursor and connection
        cur.close()
        conn.close()

        # If the item is actually 1.49$ its in the database as 149
        # if the item is actually 10.57$ its in the database as 10.57
        # is this something we need to change?

        # convert price from cents to dollars with decimal point
        price_in_dollars = Decimal(price_in_cents) / Decimal('100')
        
        return price_in_dollars
    except psycopg2.Error as e:
        print("Error fetching item price:", e)
        return None
    
def updateItemPriceInDatabase(item_id, new_price):
    try:
        # Establish connection to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cur = conn.cursor()

        # proper rounding (2.506 becomes 251 in database)
        new_price_cents = round(new_price * 100)

        # Update item price in the database
        query = """
            UPDATE storeitems
            SET price = %s
            WHERE id = %s
        """
        cur.execute(query, (new_price_cents, item_id))
        conn.commit()  # Commit the transaction

        # Close cursor and connection
        cur.close()
        conn.close()

        print("Item price updated successfully.")
    except psycopg2.Error as e:
        print("Error updating item price:", e)