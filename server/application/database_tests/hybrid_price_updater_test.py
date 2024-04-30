import unittest
from database.hybrid_price_updater import HybridPriceUpdater
from database.database import Database
from decimal import Decimal

class HybdridPriceUpdaterTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
        DB_PORT = 5432
        DB_USER = "lulapricingtest"
        DB_PASSWORD = "luladbtest"
        DB_NAME = "postgres"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.hybrid_price_updater = HybridPriceUpdater(self.db)

    def test_update_price(self):
        self.hybrid_price_updater.updateSingleItemPrice({'name': 'Coffee', 'category': 'Beverages', 'type': 'hourly', 'action': 'Decrease', 'current_price': Decimal('120'), 'suggested_price': Decimal('114.00')})
    
if __name__ == "__main__":
    unittest.main()
