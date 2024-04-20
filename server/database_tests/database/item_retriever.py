from .database import Database
import psycopg2


class ItemRetriever(Database):
    def __init__(self, db):
        self.db = db

    def getItemsByCategory(self, category):
        conn = None
        cur = None
        try:
            conn = self.db.connect()
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
            self.db.close(conn, cur)

    def getItems(self, limit=20):
        conn = None
        cur = None
        try:
            conn = self.db.connect()
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
            self.db.close(conn, cur)