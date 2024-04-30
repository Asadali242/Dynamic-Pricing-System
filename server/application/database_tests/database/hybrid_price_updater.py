from .database_helpers import DatabaseHelpers
from .price_history_updater import PriceHistoryUpdater
from decimal import Decimal

class HybridPriceUpdater:
    def __init__(self, db):
        self.db = db

    def updateSingleItemPrice(self, item_details):
        helper = DatabaseHelpers(self.db)
        price_history_updater = PriceHistoryUpdater(self.db)
        
        # Retrieve item details from the dictionary
        item_name = item_details.get('name')
        suggested_price = Decimal(item_details.get('suggested_price'))
        current_price = Decimal(item_details.get('current_price'))
        type = (item_details.get('type'))

        # Fetch the item's ID from the database using its name
        item_id = helper.fetchItemIdByName(item_name)

        # Update the item's price in the database
        helper.updateItemPriceInDatabase(item_id, suggested_price/100)

        # Add a new entry to the price history table
        price_history_updater.addPriceHistoryEntry(item_id, current_price/100, suggested_price/100, rule={'hybrid': ('hybrid', type)})
