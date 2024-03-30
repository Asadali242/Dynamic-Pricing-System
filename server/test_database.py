from database import getItemsByCategory, getItems, updateManualTimeRuleForCategory
import json
import unittest

class TestDatabaseFunctions(unittest.TestCase):
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



    #sample time rule data
    rule_data = {
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
    rule_data_json = json.dumps(rule_data)

    #default time rule data
    default_rule_data = {
        "active": False,
        "durationInDays": None,
        "priceMax": None,
        "priceMin": None,
        "timeZone": "",
        "hourlyPriceChanges": {}
    }
    default_rule_data_json = json.dumps(default_rule_data)

    #update manual_time_rule for all store-items in a category
    update_manual_time_rule_result = updateManualTimeRuleForCategory('Beverages', default_rule_data_json)
    if update_manual_time_rule_result:
        print("Manual time rule updated successfully.")
    else:
        print("Failed to update manual time rule.")

if __name__ == '__main__':
    unittest.main()