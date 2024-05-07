import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from decimal import Decimal, getcontext
from .database import Database
from .sales_history_getter import SalesHistoryGetter

class HybridSeasonalSuggestion(Database):
    def __init__(self, db):
        self.db = db
        self.scaler = StandardScaler()
        self.model = self.train_model()

    def train_model(self):
        sales_history_getter = SalesHistoryGetter(self.db)
        # Gather comprehensive data across all seasons for training
        all_seasons = ["Winter", "Spring", "Summer", "Fall"]
        data = {}
        for season in all_seasons:
            data.update(sales_history_getter.fetchDataForSeasonRuleRecommendations(season))

        if not data:
            print("No data available for model training.")
            return None

        X, y = [], []
        for category, items in data.items():
            for item_name, item_data in items.items():
                qty_season = float(item_data['averageQuantityCurrentSeason'])
                price_season = float(item_data['averagePriceThisSeason'])
                qty_overall = float(item_data['overallAverageQuantityAnyGivenSeason'])
                price_overall = float(item_data['overallAveragePriceAnyGivenSeason'])

                # Calculate the factor and limit it to ±10%
                factor = (price_season - price_overall) / price_overall
                factor = np.clip(factor, -0.05, 0.05)
                X.append([qty_season, price_season, qty_overall, price_overall])
                y.append(factor + 1)  # Adjust to the range 0.9 to 1.1

        X = np.array(X)
        y = np.array(y)
        if not X.size:
            return None

        # Train the model using linear regression
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        model = LinearRegression()
        model.fit(X_scaled, y)
        return model

    def suggest_price_change(self, season):
        # Fetch data for the specified season
        sales_history_getter = SalesHistoryGetter(self.db)
        data = sales_history_getter.fetchDataForSeasonRuleRecommendations(season)
        if not data:
            print(f"No data available to suggest price changes for season: {season}")
            return {}

        recommendations = {}
        getcontext().prec = 6

        for category, items in data.items():
            category_recommendations = []
            for item_name, item_data in items.items():
                features = np.array([
                    [float(item_data['averageQuantityCurrentSeason']),
                     float(item_data['averagePriceThisSeason']),
                     float(item_data['overallAverageQuantityAnyGivenSeason']),
                     float(item_data['overallAveragePriceAnyGivenSeason'])]
                ])

                # Predict the factor using the trained model
                features_scaled = self.scaler.transform(features)
                predicted_factor = self.model.predict(features_scaled)[0]
                current_price = Decimal(item_data['currentPrice'])
                suggested_price = current_price * Decimal(predicted_factor)

                action = 'Increase' if predicted_factor > 1 else 'Decrease' if predicted_factor < 1 else 'No Change'
                percentage_change = (Decimal(predicted_factor) - Decimal(1)) * Decimal(100)

                category_recommendations.append({
                    'name': item_name,
                    'category': category,
                    'type': "seasonal",
                    'action': action,
                    'Percentage': f"{percentage_change:.2f}%",
                    'current_price': current_price,
                    'suggested_price': round(suggested_price, 2)
                })

            recommendations[category] = category_recommendations

        return recommendations
