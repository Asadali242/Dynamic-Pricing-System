from .database import Database
from datetime import datetime, timedelta
from .database_helpers import DatabaseHelpers
import json
import psycopg2


class PriceChangeHistoryGetter(Database):
    def __init__(self, db):
        self.db = db
        self.database_helpers = DatabaseHelpers(self.db)

    def getPriceChangeHistoryForItem(self, itemID):
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = """
                SELECT createdate, price_update, rule
                FROM pricehistory
                WHERE store_item_id = %s
            """
            cur.execute(query, (itemID,))

            rows = cur.fetchall()

            cur.close()
            conn.close()

            price_history = []
            for row in rows:
                createdate = row[0]
                price_update = row[1]
                rule = row[2] 
                price_history.append({'createdate': createdate, 'price_update': price_update, 'rule': rule})

            return price_history
        except psycopg2.Error as e:
            print("Error fetching active manual hour rule store items:", e)
            return []   