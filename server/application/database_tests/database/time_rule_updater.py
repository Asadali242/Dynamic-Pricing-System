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