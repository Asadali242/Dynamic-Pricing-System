import psycopg2
from psycopg2 import Error
import json
import datetime
from database_helper_functions import getCurrentHour, fetchActiveManualHourRuleStoreItems, fetchItemPriceFromDatabase, updateItemPriceInDatabase
from decimal import Decimal

#connection parameter definitions
DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "lulapricingtest"
DB_PASSWORD = "luladbtest"
DB_NAME = "postgres"

def getItemsByCategory(category):
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
            SELECT si.id AS store_item_id, si.name AS store_item_name, si.price AS store_item_price
            FROM storeitems si
            JOIN storeitemcategories sic ON si.id = sic.store_item_id
            JOIN categories c ON sic.category_id = c.id
            WHERE c.name = %s
        """
        cur.execute(query, (category,))
        items = cur.fetchall()
        cur.close()
        conn.close()
        return items
    except psycopg2.Error as e:
        print("Error fetching items:", e)
        return []
    
def getItems(limit=20):
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
            SELECT si.id AS store_item_id, si.name AS store_item_name, si.price AS store_item_price
            FROM storeitems si
            ORDER BY si.name
            LIMIT %s
        """
        cur.execute(query, (limit,))
        items = cur.fetchall()
        cur.close()
        conn.close()
        return items
    except psycopg2.Error as e:
        print("Error fetching items:", e)
        return []

def updateManualTimeRuleForCategory(category, rule_data):
    try:
        # retrieve all items in the specified category
        items = getItemsByCategory(category)
        # update manual_time_rule for each item
        for item in items:
            item_id = item[0]
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cur = conn.cursor()
            update_query = """
                UPDATE storeitems
                SET manual_time_rule = %s
                WHERE id = %s
            """
            cur.execute(update_query, (rule_data, item_id))
            conn.commit()
            cur.close()
            conn.close()
        return True
    except psycopg2.Error as e:
        print("Error updating manual_time_rule:", e)
        return False

def updateManualSeasonalityRuleForCategory(category, rule_data):
    try:
        # retrieve all items in the specified category
        items = getItemsByCategory(category)
        # update manual_time_rule for each item
        for item in items:
            item_id = item[0]
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            cur = conn.cursor()
            update_query = """
                UPDATE storeitems
                SET manual_seasonality_rule = %s
                WHERE id = %s
            """
            cur.execute(update_query, (rule_data, item_id))
            conn.commit()
            cur.close()
            conn.close()
        return True
    except psycopg2.Error as e:
        print("Error updating manual_seasonality_rule:", e)
        return False


def manualHourlyPriceUpdate():
    relevant_store_items = fetchActiveManualHourRuleStoreItems()
    for item_id, manual_time_rule in relevant_store_items:
        hourly_price_changes = manual_time_rule.get('hourlyPriceChanges', [])
        time_zone = manual_time_rule.get('timeZone')
        current_hour = getCurrentHour(time_zone)

        print(f"Item ID: {item_id}")
        print("Time Zone:", time_zone)
        print("Current Hour (Adjusted):", current_hour)

        for change in hourly_price_changes:
            rule_hour = int(change['timestamp'].split(':')[0])
            print("Rule Hour", rule_hour)

            if rule_hour == current_hour:
                print("Current hour matches rule hour.")
                #change item's price based on the change type and percent
                if change['type'] == '+':
                    item_price = fetchItemPriceFromDatabase(item_id)
                    print("Current item price:", item_price)
                    new_price = item_price * (Decimal('1') + Decimal(change['percent']) / Decimal('100'))
                    print("New item price:", new_price)
                    updateItemPriceInDatabase(item_id, new_price)

                    #add func to add price change history info to price history table
                elif change['type'] == '-':
                    # Assuming item price is fetched from database
                    item_price = fetchItemPriceFromDatabase(item_id)
                    print("Current item price:", item_price)
                    new_price = item_price * (Decimal('1') - Decimal(change['percent']) / Decimal('100'))
                    print("New item price:", new_price)
                    updateItemPriceInDatabase(item_id, new_price)

                    #add func to add price change history info to price history table
