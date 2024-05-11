import unittest
from database.time_rule_updater import TimeRuleUpdater
from database.database import Database
import json
from datetime import datetime, timedelta

class TimeRuleUpdaterTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
        DB_PORT = 5432
        DB_USER = "lulapricingtest"
        DB_PASSWORD = "luladbtest"
        DB_NAME = "postgres"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.time_rule_updater = TimeRuleUpdater(self.db)
        dateOfCreation = datetime.now()
        dateOfCreationStr = dateOfCreation.isoformat()

        expiration_date = dateOfCreation + timedelta(3)
        expirationDateStr = expiration_date.isoformat()
        #default time of day rule data
        self.default_time_rule_data = {
            "active": False,
            "durationInDays": 1,
            "priceMax": None,
            "priceMin": None,
            "timeZone": "",
            "createDate" : None,
            "hourlyPriceChanges": {}
        }
        #sample time rule data
        self.sample_time_rule_data = {
            "active": True,
            "durationInDays": 3,
            "priceMax": 10,
            "priceMin": 4,
            "timeZone": "EST",
            "createDate" : dateOfCreationStr,
            "expirationDate": expirationDateStr,
            "hourlyPriceChanges": {
                "1:00": {"type": "+", "percent": 1},
                "2:00": {"type": "-", "percent": 2},
                "3:00": {"type": "+", "percent": 3},
                "24:00": {"type": "+", "percent": 4}
            }
        }

    def test_update_manual_time_rule_for_category(self):
        #time rule database update test
        default_time_rule_data_json = json.dumps(self.default_time_rule_data)
        sample_time_rule_data_json = json.dumps(self.sample_time_rule_data)
        update_manual_time_rule_result = self.time_rule_updater.updateManualTimeRuleForCategory('Beverages', sample_time_rule_data_json)
        if update_manual_time_rule_result:
            print("Manual time rule updated successfully.")
        else:
            print("Failed to update manual time rule.")

    '''def test_z_restore_time_rule_defaults_for_category(self):
        #clear time rule data test
        restore_time_rule_defaults_for_category = self.time_rule_updater.restoreTimeRuleDefaultsForCategory('Snacks')
        if restore_time_rule_defaults_for_category:
            print("reset seasonalityrules for snacks")
        else:
            print("Failed to reset seasonality rules for snacks") 
'''
    '''def test_get_remaining_days_for_category(self):
        get_remaining_days = self.time_rule_updater.getRemainingTimeForCategory("Snacks")
        if get_remaining_days:
            print("days left for snack rule:", get_remaining_days)
        else:
            print("Failed get remaining days for snacks") '''
        

if __name__ == "__main__":
    unittest.main()