from .database import Database
import psycopg2


class TotalSalesRetriever(Database):
    def __init__(self, db):
        self.db = db

    def calculate_total_sales(self):
        conn = None
        cur = None
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = "SELECT TO_CHAR(FLOOR(SUM(store_item_total_price) / 100.0), 'FM999,999,999') AS Formatted_Average_Price FROM orderitems;"
            cur.execute(query)
            total_sales = cur.fetchone()[0]
            print(total_sales)
            return total_sales
        except psycopg2.Error as e:
            print("Error executing query:", e)
        finally:
            self.db.close(conn, cur)