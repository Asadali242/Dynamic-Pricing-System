import unittest
from database.season_rule_updater import SeasonRuleUpdater
from database.database import Database
import json
from datetime import datetime, timedelta

class SeasonRuleUpdaterTest(unittest.TestCase):
    def setUp(self):
        # Initialize any resources needed for the tests
        DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
        DB_PORT = 5432
        DB_USER = "lulapricingtest"
        DB_PASSWORD = "luladbtest"
        DB_NAME = "postgres"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.season_rule_updater = SeasonRuleUpdater(self.db)
        dateOfCreation = datetime.now()
        dateOfCreationStr = dateOfCreation.isoformat()
        expiration_date = dateOfCreation + timedelta(days=365 * 3)
        expirationDateStr = expiration_date.isoformat()
        #default seasonality rule data
        self.default_seasonality_rule_data = {
            "active": False,
            "durationInYears": 0,
            "priceMax": None,
            "priceMin": None,
            "timeZone": "",
            "createDate" : None,
            "seasonalPriceChanges": {},
        }
        #sample seasonality rule data
        self.sample_seasonality_rule_data = {
            "active": True,
            "durationInYears": 3,
            "priceMax": 10,
            "priceMin": 4,
            "timeZone": "EST",
            "createDate" : dateOfCreationStr,
            "expirationDate": expirationDateStr,
            "seasonalPriceChanges": [
                {"season": "Spring", "type": "+", "percent": 1},
                {"season": "Summer", "type": "-", "percent": 2},
                {"season": "Fall", "type": "+", "percent": 4},
                {"season": "Winter", "type": "+", "percent": 3}
            ]
        }

    def test_update_manual_seasonality_rule_for_category(self):
        #seasonality rule database update test
        default_seasonality_rule_data_json = json.dumps(self.default_seasonality_rule_data)
        sample_seasonality_rule_data_json = json.dumps(self.sample_seasonality_rule_data)
        update_manual_seasonality_rule_result = self.season_rule_updater.updateManualSeasonalityRuleForCategory('Beverages', sample_seasonality_rule_data_json)
        if update_manual_seasonality_rule_result:
            print("Manual seasonality rule updated successfully.")
        else:
            print("Failed to update manual seasonality rule.")

    '''def test_z_restore_seasonality_rule_defaults_for_category(self):
        #clear seasonality rule data test
        restore_seasonality_rule_defaults_for_category = self.season_rule_updater.restoreSeasonalityRuleDefaultsForCategory('Snacks')
        if restore_seasonality_rule_defaults_for_category:
            print("reset seasonalityrules for snacks")
        else:
            print("Failed to reset seasonality rules for snacks") '''
        


if __name__ == "__main__":
    unittest.main()