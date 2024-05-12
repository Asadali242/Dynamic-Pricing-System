import unittest
from database.price_change_history_getter import PriceChangeHistoryGetter
from database.database import Database

class PriceChangeHistoryGetterTest(unittest.TestCase):
    def setUp(self):
        DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
        DB_PORT = 5432
        DB_USER = "lulapricingtest"
        DB_PASSWORD = "luladbtest"
        DB_NAME = "postgres"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.price_change_history_getter = PriceChangeHistoryGetter(self.db)

    def test_get_price_change_history(self):
        print("Price history for ruffles: ", self.price_change_history_getter.getPriceChangeHistoryForItem("10000000-0000-0000-0000-000000000000"))


if __name__ == "__main__":
    unittest.main()