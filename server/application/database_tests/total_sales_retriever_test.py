import unittest
from database.total_sales_retriever import TotalSalesRetriever
from database.database import Database




class TotalSalesRetrieverTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "hostname"
        DB_PORT = 0000
        DB_USER = "username"
        DB_PASSWORD = "password"
        DB_NAME = "dbname"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.total_sales_retriever = TotalSalesRetriever(self.db)

    def test_calculate_total_products_sold(self):
        print("Testing calculation of sales number")
        self.total_sales_retriever.calculate_total_sales()

if __name__ == "__main__":
    unittest.main()