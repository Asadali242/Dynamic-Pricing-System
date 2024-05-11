from .database import Database
from datetime import datetime, timedelta
from .database_helpers import DatabaseHelpers
import json


class ExpiredRuleWiper(Database):
    def __init__(self, db):
        self.db = db
        self.database_helpers = DatabaseHelpers(self.db)

    def wipeExpiredRules(self):
        conn = None
        cur = None
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            current_date = datetime.now()
            active_hour_rule_store_items = self.database_helpers.fetchActiveManualHourRuleStoreItems()
            for item in active_hour_rule_store_items:
                item_id = item[0]
                manual_time_rule = item[3]
                expiration_date = manual_time_rule.get('expirationDate') if manual_time_rule else None
                if expiration_date and datetime.fromisoformat(expiration_date) <= current_date:
                    # Reset time rule to default
                    self.resetTimeRuleToDefault(item_id)

            active_season_rule_store_items = self.database_helpers.fetchActiveManualSeasonalityRuleStoreItems()
            for item in active_season_rule_store_items:
                item_id = item[0]
                manual_seasonality_rule = item[3]
                expiration_date = manual_seasonality_rule.get('expirationDate') if manual_seasonality_rule else None
                if expiration_date and datetime.fromisoformat(expiration_date) <= current_date:
                    # Reset seasonality rule to default
                    self.resetSeasonalityRuleToDefault(item_id)

        except Exception as e:
            print("Error adding price history entry:", e)
        finally:
            self.db.close(conn, cur)

    def resetTimeRuleToDefault(self, item_id):
        try:
            conn = self.db.connect()
            cur = conn.cursor()

            # Default time rule data
            default_time_rule_data = {
                "active": False,
                "durationInDays": 1,
                "priceMax": None,
                "priceMin": None,
                "timeZone": "",
                "createDate" : None,
                "hourlyPriceChanges": {}
            }

            # Update store item with default time rule data
            cur.execute("""
                UPDATE storeitems
                SET manual_time_rule = %s
                WHERE id = %s
            """, (json.dumps(default_time_rule_data), item_id))

            conn.commit()
        except Exception as e:
            print("Error resetting time rule to default:", e)
        finally:
            self.db.close(conn, cur)

    def resetSeasonalityRuleToDefault(self, item_id):
        try:
            conn = self.db.connect()
            cur = conn.cursor()

            # Default seasonality rule data
            default_seasonality_rule_data = {
                "active": False,
                "durationInYears": 0,
                "priceMax": None,
                "priceMin": None,
                "timeZone": "",
                "createDate" : None,
                "seasonalPriceChanges": {}
            }

            # Update store item with default seasonality rule data
            cur.execute("""
                UPDATE storeitems
                SET manual_seasonality_rule = %s
                WHERE id = %s
            """, (json.dumps(default_seasonality_rule_data), item_id))

            conn.commit()
        except Exception as e:
            print("Error resetting seasonality rule to default:", e)
        finally:
            self.db.close(conn, cur)
        