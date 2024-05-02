from database_tests.database.database import Database
from database_tests.database.item_retriever import ItemRetriever
from database_tests.database.time_rule_updater import TimeRuleUpdater
from database_tests.database.season_rule_updater import SeasonRuleUpdater
from database_tests.database.sales_history_getter import SalesHistoryGetter
from database_tests.database.manual_hour_price_updater import ManualHourPriceUpdater
from database_tests.database.manual_season_price_updater import ManualSeasonPriceUpdater
from database_tests.database.price_history_updater import PriceHistoryUpdater
from database_tests.database.hybrid_time_suggestion import HybridTimeSuggestion
from database_tests.database.hybrid_price_updater import HybridPriceUpdater
from database_tests.database.total_units_sold_retriever import TotalUnitsSoldRetriever
from database_tests.database.database_helpers import DatabaseHelpers


DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "lulapricingtest"
DB_PASSWORD = "luladbtest"
DB_NAME = "postgres"
db = Database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
item_retriever = ItemRetriever(db)
time_rule_updater = TimeRuleUpdater(db)
season_rule_updater = SeasonRuleUpdater(db)
manual_hour_price_updater = ManualHourPriceUpdater(db)
manual_season_price_updater = ManualSeasonPriceUpdater(db)
sales_history_getter = SalesHistoryGetter(db)
price_history_updater = PriceHistoryUpdater(db)
hybrid_hour_suggester = HybridTimeSuggestion(db)
hybrid_price_updater = HybridPriceUpdater(db)
total_units_sold_retriever = TotalUnitsSoldRetriever(db)
database_helpers = DatabaseHelpers(db)
