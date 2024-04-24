from decimal import Decimal, getcontext
from .database import Database
from .sales_history_getter import SalesHistoryGetter

class HybridTimeSuggestion(Database):
    def __init__(self, db):
        self.db = db
        

    def suggest_price_change(self, user_hour):
        sales_history_getter = SalesHistoryGetter(self.db)
        data = sales_history_getter.fetchDataForTimeRuleRecommendations()
        if not data:
            print("No data available to suggest price changes.")
            return {}

        recommendations = {}
        getcontext().prec = 6  # Set precision for Decimal operations

        for category, items in data.items():
            category_recommendations = []
            for item_name, item_data in items.items():
                current_price = Decimal(item_data['currentPrice'])
                avg_quantity_this_hour = Decimal(item_data['monthsAverageQuantityCurrentHour'])
                avg_quantity_overall = Decimal(item_data['monthsOverallAverageQuantityAnyGivenHour'])
                avg_price_overall = Decimal(item_data['monthsOverallAveragePriceAnyGivenHour'])
                avg_price_this_hour = Decimal(item_data['monthsAveragePriceThisHour'])

                action = 'No Change'
                suggested_price = current_price

                if avg_quantity_this_hour > avg_quantity_overall:
                    suggested_price = current_price * Decimal('1.05')
                    action = 'Increase'
                elif avg_quantity_this_hour < avg_quantity_overall:
                    suggested_price = current_price * Decimal('0.95')
                    action = 'Decrease'

                if current_price > avg_price_overall * Decimal('1.05'):
                    suggested_price = avg_price_overall
                    action = 'Decrease'
                elif current_price < avg_price_overall * Decimal('0.95'):
                    suggested_price = avg_price_overall
                    action = 'Increase'

                category_recommendations.append({
                    'name': item_name,
                    'action': action,
                    'current_price': current_price,
                    'suggested_price': round(suggested_price, 2)
                })

            recommendations[category] = category_recommendations

        return recommendations
