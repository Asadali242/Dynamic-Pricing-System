import datetime
import psycopg2
from datetime import datetime
import datetime
from psycopg2 import Error
import pytz
from decimal import Decimal
from .database import Database


class DatabaseHelpers(Database):
    def __init__(self, db):
        self.db = db

    #return current hour given timezone
    def getCurrentHour(self, timezone):
        if timezone.upper() == 'EST':
            timezone = 'US/Eastern'
        if timezone.upper() == 'PST':
            timezone = 'US/Pacific'
        current_time = datetime.datetime.now(pytz.timezone(timezone))
        return current_time.hour

    #return any store item that has an active hour rule
    def fetchActiveManualHourRuleStoreItems(self):
        try:
            conn = self.db.connect()
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

    #return any store item that has an active season rule
    def fetchActiveManualSeasonalityRuleStoreItems(self):
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = query = """
                SELECT id, manual_seasonality_rule
                FROM storeitems
                WHERE manual_seasonality_rule->>'active' = 'true'
            """
            cur.execute(query)
            relevant_store_items = cur.fetchall()
            cur.close()
            conn.close()
            return relevant_store_items
        except psycopg2.Error as e:
            print("Error fetching active manual seasonality rule store items:", e)
            return []

    #return current price of given store item
    def fetchItemPriceFromDatabase(self, item_id):
        try:
            # Establish connection to the database
            conn = self.db.connect()
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
        
    #update current price of given store item
    def updateItemPriceInDatabase(self, item_id, new_price):
        try:
            # Establish connection to the database
            conn = self.db.connect()
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

    def fetchItemIdByName(self, item_name):
        conn = self.db.connect()
        cur = conn.cursor()
        query = "SELECT id FROM storeitems WHERE name = %s;"
        cur.execute(query, (item_name,))
        result = cur.fetchone()
        cur.close()
        if result:
            return result[0] 
        else:
            raise ValueError(f"No item found with the name '{item_name}'")