import unittest
from database.database import Database
from database.hybrid_seasonal_suggestion import HybridSeasonalSuggestion

class HybridSeasonalSuggestionTest(unittest.TestCase):
    def setUp(self):
        DB_HOST = "hostname"
        DB_PORT = 0000
        DB_USER = "username"
        DB_PASSWORD = "password"
        DB_NAME = "dbname"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.hybrid_seasonal_suggestion = HybridSeasonalSuggestion(self.db)

    def test_model_availability(self):
        self.assertTrue(self.hybrid_seasonal_suggestion.model, "Model should be trained and available.")
        print("Model availability check passed.")

    def test_suggest_price_change(self):
        print("Testing suggest_price_change for a specific season...")
        # Use a valid season name like "Winter", "Spring", "Summer", or "Fall"
        suggestions = self.hybrid_seasonal_suggestion.suggest_price_change("Summer")
        self.assertIsInstance(suggestions, dict, "Suggestions should be returned as a dictionary.")
        self.assertTrue(suggestions, "Suggestions should not be empty.")

        print("Suggestions made successfully.")
        for category, items in suggestions.items():
            print(f"Category: {category}")
            for item in items:
                print(f"Item: {item['name']}, Category: {item['category']}, Type: {item['type']}, Action: {item['action']}, Percentage: {item['Percentage']}, Current Price: {item['current_price']}, Suggested Price: {item['suggested_price']}")

if __name__ == "__main__":
    unittest.main()
