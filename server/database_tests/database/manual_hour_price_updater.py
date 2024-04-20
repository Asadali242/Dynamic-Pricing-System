from .database import Database
import psycopg2
from .database_helpers import DatabaseHelpers
from .price_history_updater import PriceHistoryUpdater
from decimal import Decimal


class ManualHourPriceUpdater(Database):
    def __init__(self, db):
        self.db = db

    def manualHourlyPriceUpdate(self):
        helper = DatabaseHelpers(self.db)
        price_history_updater = PriceHistoryUpdater(self)
        relevant_store_items = helper.fetchActiveManualHourRuleStoreItems()
        for item_id, manual_time_rule in relevant_store_items:
            hourly_price_changes = manual_time_rule.get('hourlyPriceChanges', [])
            time_zone = manual_time_rule.get('timeZone')
            current_hour = helper.getCurrentHour(time_zone)

            print(f"Item ID: {item_id}")
            print("Time Zone:", time_zone)
            print("Current Hour (Adjusted):", current_hour)

            for change in hourly_price_changes:
                rule_hour = int(change['timestamp'].split(':')[0])
                print("Rule Hour", rule_hour)

                if rule_hour == current_hour:
                    print("Current hour matches rule hour.")
                    #change item's price based on the change type and percent
                    if change['type'] == '+':
                        item_price = helper.fetchItemPriceFromDatabase(item_id)
                        print("Current item price:", item_price)
                        new_price = item_price * (Decimal('1') + Decimal(change['percent']) / Decimal('100'))
                        print("New item price:", new_price)
                        helper.updateItemPriceInDatabase(item_id, new_price)
                        
                        #func to add price change history info to price history table
                        price_history_updater.addPriceHistoryEntry(item_id, item_price, new_price, rule={'manual': ('manual', 'time-based')})
                        
                    elif change['type'] == '-':
                        # Assuming item price is fetched from database
                        item_price = helper.fetchItemPriceFromDatabase(item_id)
                        print("Current item price:", item_price)
                        new_price = item_price * (Decimal('1') - Decimal(change['percent']) / Decimal('100'))
                        print("New item price:", new_price)
                        helper.updateItemPriceInDatabase(item_id, new_price)

                        #func to add price change history info to price history table
                        price_history_updater.addPriceHistoryEntry(item_id, item_price, new_price, rule={'manual': ('manual', 'time-based')})
                    