from .database import Database
import psycopg2
from .item_retriever import ItemRetriever
import json
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
scheduler = BackgroundScheduler()
category_timers_seasonality = {}

class SeasonRuleUpdater(Database):

    def __init__(self, db):
        self.db = db

    def updateManualSeasonalityRuleForCategory(self, category, rule_data):
        conn = None
        cur = None
        itemRetriever = ItemRetriever(self.db)
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
                timer = scheduler.add_job(self.restoreSeasonalityRuleDefaultsForCategory, 'date', run_date=expiry_datetime, args=[category])
                category_timers_seasonality[category] = timer
                print("Timer scheduled for category:", category)
                print("Timer info:", timer)
            
            # retrieve all items in the specified category
            items = itemRetriever.getItemsByCategory(category)
            # update manual_time_rule for each item
            for item in items:
                item_id = item[0]
                conn = self.db.connect()
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
            self.db.close(conn, cur)

    def restoreSeasonalityRuleDefaultsForCategory(self, category):
        conn = None
        cur = None
        itemRetriever = ItemRetriever(self.db)
        global category_timers_time
        default_seasonality_rule_data = {
            "active": False,
            "durationInYears": None,
            "priceMax": None,
            "priceMin": None,
            "timeZone": "",
            "createDate" : None,
            "seasonalPriceChanges": {}
        }
        try:
            default_seasonality_rule_json = json.dumps(default_seasonality_rule_data)
            # retrieve all items in the specified category
            items = itemRetriever.getItemsByCategory(category)
            # update manual_time_rule for each item
            for item in items:
                item_id = item[0]
                conn = self.db.connect()
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
            self.db.close(conn, cur)