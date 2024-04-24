import unittest
from database.database import Database
from database.hybrid_time_suggestion import HybridTimeSuggestion


class HybridTimeSuggestionTest(unittest.TestCase):
    def setUp(self):
        DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
        DB_PORT = 5432
        DB_USER = "lulapricingtest"
        DB_PASSWORD = "luladbtest"
        DB_NAME = "postgres"
        self.db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
        self.hybrid_time_suggestion = HybridTimeSuggestion(self.db)


    def test_suggest_price_change(self):
        print("Testing suggest_price_change...")
        # Assuming user_time for test purposes is set statically, e.g., 12
        suggestions = self.hybrid_time_suggestion.suggest_price_change(12)
        self.assertIsInstance(suggestions, dict, "Suggestions should be a dictionary.")
        print("Suggestions made successfully.")
        print("Suggestions Output:")
        for category, items in suggestions.items():
            print(f"Category: {category}")
            for item in items:
                print(f"Item: {item['name']}, Action: {item['action']}, Current Price: {item['current_price']}, Suggested Price: {item['suggested_price']}")


if __name__ == "__main__":
    unittest.main()
