import unittest
from database.manual_hour_price_updater import ManualHourPriceUpdater
from database.database import Database

class ManualHourPriceUpdaterTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "hostname"
        DB_PORT = 0000
        DB_USER = "username"
        DB_PASSWORD = "password"
        DB_NAME = "dbname"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.manual_hour_price_updater= ManualHourPriceUpdater(self.db)

    
    #hourly price update test
    def test_hourly_price_update_display(self):
        print("Running test for manualHourlyPriceUpdate function...")
        #careful, the below function will actually change database price values if there is a time rule for this hour
        self.manual_hour_price_updater.manualHourlyPriceUpdate()
        print("Test for manualHourlyPriceUpdate function completed.")
    


if __name__ == "__main__":
    unittest.main()