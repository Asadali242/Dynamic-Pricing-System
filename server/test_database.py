from database import restoreTimeRuleDefaultsForCategory, restoreSeasonalityRuleDefaultsForCategory, updateManualSeasonalityRuleForCategory, getItemsByCategory, getItems, updateManualTimeRuleForCategory, manualHourlyPriceUpdate
import json
import unittest

class TestDatabaseFunctions(unittest.TestCase):
    #default seasonality rule data
    default_seasonality_rule_data = {
        "active": False,
        "durationInYears": None,
        "priceMax": None,
        "priceMin": None,
        "timeZone": "",
        "seasonalPriceChanges": {}
    }

    #default time of day rule data
    default_time_rule_data = {
        "active": False,
        "durationInDays": None,
        "priceMax": None,
        "priceMin": None,
        "timeZone": "",
        "hourlyPriceChanges": {}
    }

    #sample time rule data
    sample_time_rule_data = {
        "active": True,
        "durationInDays": 3,
        "priceMax": 10,
        "priceMin": 4,
        "timeZone": "EST",
        "hourlyPriceChanges": {
            "1:00": {"type": "+", "percent": 1},
            "2:00": {"type": "-", "percent": 2},
            "3:00": {"type": "+", "percent": 3},
            "24:00": {"type": "+", "percent": 4}
        }
    }


    #list all store-items in chicken category
    items = getItemsByCategory('Chicken')
    for item in items:
        print(item)
    print("\n")

    #list first 5 items in store-items by alphabetical order
    items = getItems(5)
    for item in items:
        print(item)
    print("\n")

    #time rule database update test
    sample_time_rule_data_json = json.dumps(sample_time_rule_data)
    default_time_rule_data_json = json.dumps(default_time_rule_data)

    update_manual_time_rule_result = updateManualTimeRuleForCategory('Snacks', sample_time_rule_data_json)
    if update_manual_time_rule_result:
        print("Manual time rule updated successfully.")
    else:
        print("Failed to update manual time rule.")

    #seasonality rule database update test
    default_seasonality_rule_data_json = json.dumps(default_seasonality_rule_data)
    update_manual_seasonality_rule_result = updateManualSeasonalityRuleForCategory('Snacks', default_seasonality_rule_data_json)
    if update_manual_seasonality_rule_result:
        print("Manual seasonality rule updated successfully.")
    else:
        print("Failed to update manual seasonality rule.")

    #clear time rule data test
    restore_time_rule_defaults_for_category = restoreTimeRuleDefaultsForCategory('Snacks')
    if restore_time_rule_defaults_for_category:
        print("reset time of day rules for snacks")
    else:
        print("Failed to reset time of day rules for snacks")

    #clear seasonality rule data test
    restore_seasonality_rule_defaults_for_category = restoreSeasonalityRuleDefaultsForCategory('Snacks')
    if restore_seasonality_rule_defaults_for_category:
        print("reset seasonalityrules for snacks")
    else:
        print("Failed to reset seasonality rules for snacks") 
    
    #hourly price update test
    def test_hourly_price_update_display(self):
        print("Running test for manualHourlyPriceUpdate function...")
        #careful, the below function will actually change database price values if there is a time rule for this hour
        #manualHourlyPriceUpdate()
        print("Test for manualHourlyPriceUpdate function completed.")

if __name__ == '__main__':
    unittest.main()