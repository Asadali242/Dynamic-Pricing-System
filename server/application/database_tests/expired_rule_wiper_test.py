import unittest
from database.expired_rule_wiper import ExpiredRuleWiper
from database.database import Database
from decimal import Decimal

class ExpiredRuleWiperTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "hostname"
        DB_PORT = 0000
        DB_USER = "username"
        DB_PASSWORD = "password"
        DB_NAME = "dbname"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.rule_clearer = ExpiredRuleWiper(self.db)

    def test_wipe_expired_rules(self):
        print("checking for and clearing any rules that are expired")
        self.rule_clearer.wipeExpiredRules()
    
if __name__ == "__main__":
    unittest.main()
