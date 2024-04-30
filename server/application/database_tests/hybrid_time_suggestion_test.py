import unittest
from database.database import Database
from database.hybrid_time_suggestion import HybridTimeSuggestion

class HybridTimeSuggestionTest(unittest.TestCase):
    def setUp(self):
        # Configure the database connection parameters
        DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
        DB_PORT = 5432
        DB_USER = "lulapricingtest"
        DB_PASSWORD = "luladbtest"
        DB_NAME = "postgres"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.hybrid_time_suggestion = HybridTimeSuggestion(self.db)

    def test_model_availability(self):
        # Ensure models are trained and available for each item
        self.assertTrue(self.hybrid_time_suggestion.model, "Models should be trained and available for items.")
        print("Model availability check passed.")

    def test_suggest_price_change(self):
        print("Testing suggest_price_change...")
        # Assuming the current hour for test purposes is set statically, e.g., 12
        suggestions = self.hybrid_time_suggestion.suggest_price_change(21)
        self.assertIsInstance(suggestions, dict, "Suggestions should be returned as a dictionary.")
        self.assertTrue(suggestions, "Suggestions should not be empty.")
        
        print("Suggestions made successfully.")
        print("Suggestions Output:")
        for category, items in suggestions.items():
            print(f"Category: {category}")
            for item in items:
                self.assertIn('Percentage', item, "Each suggestion should include a 'Percentage' for the price adjustment.")
                print(f"Item: {item['name']}, Category: {item['category']}, Type: {item['type']}, Action: {item['action']}, Percentage: {item['Percentage']}, Current Price: {item['current_price']}, Suggested Price: {item['suggested_price']}")

if __name__ == "__main__":
    unittest.main()
