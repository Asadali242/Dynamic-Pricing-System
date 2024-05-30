import unittest
from database.price_history_updater import PriceHistoryUpdater
from database.database import Database

class PriceHistoryUpdaterTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "hostname"
        DB_PORT = 0000
        DB_USER = "username"
        DB_PASSWORD = "password"
        DB_NAME = "dbname"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.price_history_updater = PriceHistoryUpdater(self.db)

    def test_price_history_update_time(self):
        self.price_history_updater.addPriceHistoryEntry('10000000-0000-0000-0000-000000000000', 2.49, 2.99, rule={'manual': ('manual', 'time')})

    def test_price_history_update_seasonality(self):
        self.price_history_updater.addPriceHistoryEntry('10000000-0000-0000-0000-000000000000', 100, 400, rule={'manual': ('manual', 'seasonality')})

    def test_price_history_update_none(self):
        self.price_history_updater.addPriceHistoryEntry('10000000-0000-0000-0000-000000000000', 3.241, 5, rule=None)
    


if __name__ == "__main__":
    unittest.main()