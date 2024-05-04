from .database import Database
import psycopg2
from .database_helpers import DatabaseHelpers
from .price_history_updater import PriceHistoryUpdater
from decimal import Decimal

class ManualSeasonPriceUpdater(Database):
    def __init__(self, db):
        self.db = db

    def manualSeasonalPriceUpdate(self, season):
        helper = DatabaseHelpers(self.db)
        price_history_updater = PriceHistoryUpdater(self.db)
        relevant_store_items = helper.fetchActiveManualSeasonalityRuleStoreItems()
        print("relevant store items:", relevant_store_items)
        for item_id, name, price, manual_seasonality_rule in relevant_store_items:
            seasonal_price_changes = manual_seasonality_rule.get('seasonalPriceChanges', [])
            print(f"Item ID: {item_id}")
            print("Current Season:", season)
            
            # Iterate over each seasonal change dictionary
            for change in seasonal_price_changes:
                if change['season'] == season:
                    price_type = change.get('type')
                    percent_change = change.get('percent')
                    
                    # Change the item's price based on the seasonal change
                    if price_type == '+':
                        item_price = helper.fetchItemPriceFromDatabase(item_id)
                        item_price_max_seasonal = Decimal(helper.fetchSeasonalItemPriceMaxFromDatabase(item_id))
                        print("Current item price:", item_price)
                        new_price = item_price * (Decimal('1') + Decimal(percent_change) / Decimal('100'))
                        if new_price > item_price_max_seasonal:
                            new_price = item_price_max_seasonal
                        print("New item price:", new_price)
                        helper.updateItemPriceInDatabase(item_id, new_price)
                        
                        #func to add price change history info to price history table
                        price_history_updater.addPriceHistoryEntry(item_id, item_price, new_price, rule={'manual': ('manual', 'seasonality')})
                    elif price_type == '-':
                        item_price = helper.fetchItemPriceFromDatabase(item_id)
                        item_price_min_seasonal = Decimal(helper.fetchSeasonalItemPriceMinFromDatabase(item_id))
                        print("Current item price:", item_price)
                        new_price = item_price * (Decimal('1') - Decimal(percent_change) / Decimal('100'))
                        if new_price < item_price_min_seasonal:
                            new_price = item_price_min_seasonal
                        print("New item price:", new_price)
                        helper.updateItemPriceInDatabase(item_id, new_price)
                        
                        #func to add price change history info to price history table
                        price_history_updater.addPriceHistoryEntry(item_id, item_price, new_price, rule={'manual': ('manual', 'seasonality')})
                    
                    print(f"Prices updated for {season} by {percent_change}%")
                    break  # Exit the loop after finding the matching season
        
