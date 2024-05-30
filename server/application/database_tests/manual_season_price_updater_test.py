import unittest
from database.manual_season_price_updater import ManualSeasonPriceUpdater
from database.database import Database

class ManualSeasonPriceUpdaterTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "hostname"
        DB_PORT = 0000
        DB_USER = "username"
        DB_PASSWORD = "password"
        DB_NAME = "dbname"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.manual_season_price_updater = ManualSeasonPriceUpdater(self.db)

    #seasonal price update test
    def test_hourly_price_update_display(self):
        print("Running test for manualSeasonalPriceUpdate function... (winter)")
        #careful, the below function will actually change database price values if there is a time rule for this hour
        self.manual_season_price_updater.manualSeasonalPriceUpdate('Winter')
        print("Test for manualSeasonalPriceUpdate function completed.")


if __name__ == "__main__":
    unittest.main()