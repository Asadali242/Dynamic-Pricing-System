from .database import Database
import psycopg2
from .item_retriever import ItemRetriever
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
scheduler = BackgroundScheduler()
category_timers_time = {}

class TimeRuleUpdater(Database):
    def __init__(self, db):
        self.db = db

    def updateManualTimeRuleForCategory(self, category, rule_data):
        conn = None
        cur = None
        itemRetriever = ItemRetriever(self.db)
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
                timer = scheduler.add_job(self.restoreTimeRuleDefaultsForCategory, 'date', run_date=expiry_datetime, args=[category])
                category_timers_time[category] = timer
                print("Timer scheduled for category:", category)
                print("Timer info:", timer)
                print("category_timer full info1: ", category_timers_time)
            # retrieve all items in the specified category
            items = itemRetriever.getItemsByCategory(category)
            # update manual_time_rule for each item
            for item in items:
                item_id = item[0]
                conn = self.db.connect()
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
            self.db.close(conn, cur)

    def restoreTimeRuleDefaultsForCategory(self, category):
        conn = None
        cur = None
        itemRetriever = ItemRetriever(self.db)
        #global category_timers_time
        default_time_rule_data = {
            "active": False,
            "durationInDays": None,
            "priceMax": None,
            "priceMin": None,
            "timeZone": "",
            "createDate" : None,
            "hourlyPriceChanges": {}
        }
        # Update the manual time rule for the category with defaults 
        try:
            default_time_rule_json = json.dumps(default_time_rule_data)
            items = itemRetriever.getItemsByCategory(category)
            for item in items:
                item_id = item[0]
                conn = self.db.connect()
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
            self.db.close(conn, cur)

    def getRemainingTimeForCategory(self, category):
        print("category_timer full info2: ", category_timers_time)
        print("Timer info for category:", category, category_timers_time.get(category))
        if category in category_timers_time:
            expiry_datetime = category_timers_time[category].next_run_time
            print("Expiry datetime:", expiry_datetime)
            if expiry_datetime:
                remaining_time = expiry_datetime - datetime.now()
                print("Remaining time:", remaining_time)
                remaining_days = remaining_time.days
                print("Remaining days:", remaining_days)
                return remaining_days
        print("No active timer found for category:", category)
        return None