import unittest
from database.item_retriever import ItemRetriever
from database.database import Database

class ItemRetrieverTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "hostname"
        DB_PORT = 0000
        DB_USER = "username"
        DB_PASSWORD = "password"
        DB_NAME = "dbname"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.item_retriever= ItemRetriever(self.db)

    def test_get_items_by_category(self):
        print("getting items by category, snacks: ", self.item_retriever.getItemsByCategory('Snacks'))
        

    def test_get_items(self):
        print("getting items by default length, 20: ", self.item_retriever.getItems())

if __name__ == "__main__":
    unittest.main()