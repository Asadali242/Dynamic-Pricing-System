import psycopg2
from psycopg2 import Error
import json
import datetime
import database_helper_functions
from decimal import Decimal
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime, timedelta
import uuid
category_timers_time = {}
category_timers_seasonality = {}
scheduler = BackgroundScheduler()


#connection parameter definitions
DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "lulapricingtest"
DB_PASSWORD = "luladbtest"
DB_NAME = "postgres"

def connect_to_database():
    conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    return conn

def getItemsByCategory(category):
    conn = None
    cur = None
    try:
        conn = connect_to_database()
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
        return items
    except psycopg2.Error as e:
        print("Error fetching items:", e)
        return []
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    
def getItems(limit=20):
    conn = None
    cur = None
    try:
        conn = connect_to_database()
        cur = conn.cursor()
        query = """
            SELECT si.id AS store_item_id, si.name AS store_item_name, si.price AS store_item_price
            FROM storeitems si
            ORDER BY si.name
            LIMIT %s
        """
        cur.execute(query, (limit,))
        items = cur.fetchall()
        return items
    except psycopg2.Error as e:
        print("Error fetching items:", e)
        return []
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def updateManualTimeRuleForCategory(category, rule_data):
    conn = None
    cur = None
    try:
        # Logic for setting timer based on duration and ending the rule upon time elapsing
        rule_data_json = json.loads(rule_data)
        duration_in_days = int(rule_data_json.get('durationInDays', 0))
        print("Duration in days:", duration_in_days)
        
        if duration_in_days is not None:
            # If a timer already exists for these items, overwrite it
            if category in category_timers_time:
                category_timers_time[category].remove()
            
            # Calculate the datetime when the rule should be reverted back to default
            expiry_datetime = datetime.now() + timedelta(days=duration_in_days)
            
            # Schedule a one-time job to revert the rule back to default
            timer = scheduler.add_job(restoreTimeRuleDefaultsForCategory, 'date', run_date=expiry_datetime, args=[category])
            category_timers_time[category] = timer
            print("Timer scheduled for category:", category)
            print("Timer info:", timer)

        # retrieve all items in the specified category
        items = getItemsByCategory(category)
        # update manual_time_rule for each item
        for item in items:
            item_id = item[0]
            conn = connect_to_database()
            cur = conn.cursor()
            update_query = """
                UPDATE storeitems
                SET manual_time_rule = %s
                WHERE id = %s
            """
            cur.execute(update_query, (rule_data, item_id))
            conn.commit()
        return True
    except psycopg2.Error as e:
        print("Error updating manual_time_rule:", e)
        return False
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def updateManualSeasonalityRuleForCategory(category, rule_data):
    conn = None
    cur = None
    try:
        # Logic for setting timer based on duration and ending the rule upon time elapsing
        rule_data_json = json.loads(rule_data)
        duration_in_years = int(rule_data_json.get('durationInYears', 0))
        print("Duration in years:", duration_in_years)
        
        if duration_in_years is not None:
            # If a timer already exists for these items, overwrite it
            if category in category_timers_seasonality:
                category_timers_seasonality[category].remove()
                print("removing previous timers")
            
            # Calculate the datetime when the rule should be reverted back to default
            expiry_datetime = datetime.now() + timedelta(days=365 * duration_in_years)
            print("expiry_datetime:", expiry_datetime)
            
            # Schedule a one-time job to revert the rule back to default
            timer = scheduler.add_job(restoreSeasonalityRuleDefaultsForCategory, 'date', run_date=expiry_datetime, args=[category])
            category_timers_seasonality[category] = timer
            print("Timer scheduled for category:", category)
            print("Timer info:", timer)
        
        # retrieve all items in the specified category
        items = getItemsByCategory(category)
        # update manual_time_rule for each item
        for item in items:
            item_id = item[0]
            conn = connect_to_database()
            cur = conn.cursor()
            update_query = """
                UPDATE storeitems
                SET manual_seasonality_rule = %s
                WHERE id = %s
            """
            cur.execute(update_query, (rule_data, item_id))
            conn.commit()
        return True
    except psycopg2.Error as e:
        print("Error updating manual_seasonality_rule:", e)
        return False
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def manualHourlyPriceUpdate():
    relevant_store_items = database_helper_functions.fetchActiveManualHourRuleStoreItems()
    for item_id, manual_time_rule in relevant_store_items:
        hourly_price_changes = manual_time_rule.get('hourlyPriceChanges', [])
        time_zone = manual_time_rule.get('timeZone')
        current_hour = database_helper_functions.getCurrentHour(time_zone)

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
                    item_price = database_helper_functions.fetchItemPriceFromDatabase(item_id)
                    print("Current item price:", item_price)
                    new_price = item_price * (Decimal('1') + Decimal(change['percent']) / Decimal('100'))
                    print("New item price:", new_price)
                    database_helper_functions.updateItemPriceInDatabase(item_id, new_price)
                    
                    #func to add price change history info to price history table
                    addPriceHistoryEntry(item_id, item_price, new_price, rule={'manual': ('manual', 'time-based')})
                    
                elif change['type'] == '-':
                    # Assuming item price is fetched from database
                    item_price = database_helper_functions.fetchItemPriceFromDatabase(item_id)
                    print("Current item price:", item_price)
                    new_price = item_price * (Decimal('1') - Decimal(change['percent']) / Decimal('100'))
                    print("New item price:", new_price)
                    database_helper_functions.updateItemPriceInDatabase(item_id, new_price)

                    #func to add price change history info to price history table
                    addPriceHistoryEntry(item_id, item_price, new_price, rule={'manual': ('manual', 'time-based')})
                   
def manualSeasonalPriceUpdate(season):
    relevant_store_items = database_helper_functions.fetchActiveManualSeasonalityRuleStoreItems()
    print("relevant store items:", relevant_store_items)
    for item_id, manual_seasonality_rule in relevant_store_items:
        seasonal_price_changes = manual_seasonality_rule.get('seasonalPriceChanges', [])
        print(f"Item ID: {item_id}")
        print("Current Season:", season)
        
        # Iterate over each seasonal change dictionary
        for change in seasonal_price_changes:
            if change['season'] == season:
                price_type = change.get('type')
                percent_change = change.get('percent')
                
                # Change the item's price based on the seasonal change
                if price_type == '+':
                    item_price = database_helper_functions.fetchItemPriceFromDatabase(item_id)
                    print("Current item price:", item_price)
                    new_price = item_price * (Decimal('1') + Decimal(percent_change) / Decimal('100'))
                    print("New item price:", new_price)
                    database_helper_functions.updateItemPriceInDatabase(item_id, new_price)
                    
                    #func to add price change history info to price history table
                    addPriceHistoryEntry(item_id, item_price, new_price, rule={'manual': ('manual', 'seasonality')})
                elif price_type == '-':
                    item_price = database_helper_functions.fetchItemPriceFromDatabase(item_id)
                    print("Current item price:", item_price)
                    new_price = item_price * (Decimal('1') - Decimal(percent_change) / Decimal('100'))
                    print("New item price:", new_price)
                    database_helper_functions.updateItemPriceInDatabase(item_id, new_price)
                    
                    #func to add price change history info to price history table
                    addPriceHistoryEntry(item_id, item_price, new_price, rule={'manual': ('manual', 'seasonality')})
                
                print(f"Prices updated for {season} by {percent_change}%")
                break  # Exit the loop after finding the matching season
        
def restoreTimeRuleDefaultsForCategory(category):
    conn = None
    cur = None
    global category_timers_time
    default_time_rule_data = {
        "active": False,
        "durationInDays": None,
        "priceMax": None,
        "priceMin": None,
        "timeZone": "",
        "hourlyPriceChanges": {}
    }
    
    # Update the manual time rule for the category with defaults 
    try:
        default_time_rule_json = json.dumps(default_time_rule_data)
        items = getItemsByCategory(category)
        for item in items:
            item_id = item[0]
            conn = connect_to_database()
            cur = conn.cursor()
            update_query = """
                UPDATE storeitems
                SET manual_time_rule = %s
                WHERE id = %s
            """
            cur.execute(update_query, (default_time_rule_json, item_id))
            conn.commit()
        return True
    except psycopg2.Error as e:
        print("Error updating manual_time_rule:", e)
        return False
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def restoreSeasonalityRuleDefaultsForCategory(category):
    conn = None
    cur = None
    global category_timers_time
    default_seasonality_rule_data = {
        "active": False,
        "durationInYears": None,
        "priceMax": None,
        "priceMin": None,
        "timeZone": "",
        "seasonalPriceChanges": {}
    }
    try:
        default_seasonality_rule_json = json.dumps(default_seasonality_rule_data)
        # retrieve all items in the specified category
        items = getItemsByCategory(category)
        # update manual_time_rule for each item
        for item in items:
            item_id = item[0]
            conn = connect_to_database()
            cur = conn.cursor()
            update_query = """
                UPDATE storeitems
                SET manual_seasonality_rule = %s
                WHERE id = %s
            """
            cur.execute(update_query, (default_seasonality_rule_json, item_id))
            conn.commit()
        return True
    except psycopg2.Error as e:
        print("Error updating manual_seasonality_rule:", e)
        return False
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def addPriceHistoryEntry(store_item_id, price_before, price_after, rule=None):
    conn = None
    cur = None
    try:
        conn = connect_to_database()
        cur = conn.cursor()

        #random unique id for the price history entry
        price_history_id = str(uuid.uuid4())

        #prices converted from dollars to cents
        price_before_cents = int(price_before * 100)
        price_after_cents = int(price_after * 100)

        #current date and time
        createdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #JSON objects for price_update and rule
        price_update = json.dumps({'priceBefore': price_before_cents, 'priceAfter': price_after_cents})
        rule_json = json.dumps(rule) if rule else None

        #new entry into the pricehistory table
        cur.execute("""
            INSERT INTO pricehistory (id, store_item_id, createdate, price_update, rule)
            VALUES (%s, %s, %s, %s, %s)
        """, (price_history_id, store_item_id, createdate, price_update, rule_json))
        conn.commit()
        print("Price history entry added successfully with following fields:", price_history_id, store_item_id, createdate, price_update, rule_json)
    except Exception as e:
        print("Error adding price history entry:", e)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
