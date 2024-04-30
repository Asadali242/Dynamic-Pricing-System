import unittest
from database.database_helpers import DatabaseHelpers
from database.database import Database

class DatabaseHelpersTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
        DB_PORT = 5432
        DB_USER = "lulapricingtest"
        DB_PASSWORD = "luladbtest"
        DB_NAME = "postgres"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.helper = DatabaseHelpers(self.db)

    def test_get_current_hour(self):
        print("get current hour test(EST): ", self.helper.getCurrentHour('EST'))

    def test_fetch_active_manual_hour_rule_store_items(self):
        print("get items with active manual hour rules:", self.helper.fetchActiveManualHourRuleStoreItems())


    def test_fetch_active_manual_seasonality_rule_store_items(self):
        print("get items with active manual seasonality rules:", self.helper.fetchActiveManualSeasonalityRuleStoreItems())


    def test_fetch_item_price_from_database(self):
        red_bull_id = '22000000-0000-0000-0000-000000000000'
        print("get item price, red bull: ", self.helper.fetchItemPriceFromDatabase('22000000-0000-0000-0000-000000000000'))


    def test_update_item_price_in_database(self):
        red_bull_id = '22000000-0000-0000-0000-000000000000'
        #use decimal for price, updater converts to cents
        print("change price, red bull: ", self.helper.updateItemPriceInDatabase('22000000-0000-0000-0000-000000000000', 2.30))
        pass

    def test_fetch_id_by_name(self):
        print("ruffles id gotten by name:", self.helper.fetchItemIdByName("Ruffles Queso Cheese Potato Chips"))

if __name__ == "__main__":
    unittest.main()
