from .database import Database
import psycopg2
import uuid
import datetime
from datetime import datetime, timedelta
import json

class PriceHistoryUpdater(Database):
    def __init__(self, db):
        self.db = db

    def addPriceHistoryEntry(self, store_item_id, price_before, price_after, rule=None):
        conn = None
        cur = None
        try:
            conn = self.db.connect()
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
            self.db.close(conn, cur)
