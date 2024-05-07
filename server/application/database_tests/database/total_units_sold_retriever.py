from .database import Database
import psycopg2


class TotalUnitsSoldRetriever(Database):
    def __init__(self, db):
        self.db = db

    def calculate_total_products_sold(self):
        conn = None
        cur = None
        try:
            conn = self.db.connect()
            cur = conn.cursor()
            query = "SELECT TO_CHAR(FLOOR(SUM(quantity)), 'FM999,999,999') AS Formatted_Average_Quantity FROM orderitems;"
            cur.execute(query)
            total_products_sold = cur.fetchone()[0]
            print(total_products_sold)
            return total_products_sold
        except psycopg2.Error as e:
            print("Error executing query:", e)
        finally:
            self.db.close(conn, cur)
            