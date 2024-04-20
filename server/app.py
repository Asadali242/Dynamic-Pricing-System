from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import logging
import json
import schedule
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import datetime
from database_tests.database.database import Database
from database_tests.database.item_retriever import ItemRetriever
from database_tests.database.time_rule_updater import TimeRuleUpdater
from database_tests.database.season_rule_updater import SeasonRuleUpdater
from database_tests.database.sales_history_getter import SalesHistoryGetter
from database_tests.database.manual_hour_price_updater import ManualHourPriceUpdater
from database_tests.database.manual_season_price_updater import ManualSeasonPriceUpdater
from database_tests.database.price_history_updater import PriceHistoryUpdater


app = Flask(__name__)
CORS(app)

scheduler = BackgroundScheduler()
scheduler.start()

# Initialize any resources needed for the tests
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

@app.route('/items_by_category', methods=['GET'])
def items_by_category():
    try:
        category = request.args.get('category')
        items = item_retriever.getItemsByCategory(category)
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/items_by_alphabet', methods=['GET'])
def items_by_alphabet():
    try:
        limit = request.args.get('limit', default=20, type=int)
        items = item_retriever.getItems(limit)
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/create_rule', methods=['POST'])
def create_rule():
    try:
        #data from client
        data = request.json  
        print(data, flush=True)
        #parse data from client
        ruleType = data.get('ruleType')
        category = data.get('category')
        duration = data.get('duration')
        priceMaximum = data.get('priceMaximum')
        priceMinimum = data.get('priceMinimum')
        timezone = data.get('timezone')
        hourlyPriceChanges = data.get('hourlyPriceChanges')
        seasonalPriceChanges = data.get('seasonalPriceChanges')
        
        if ruleType == "TimeOfDay":
            manual_time_rule_data = {
                "active": True,  
                "durationInDays": duration,
                "priceMax": priceMaximum,
                "priceMin": priceMinimum,
                "timeZone": timezone,
                "hourlyPriceChanges": hourlyPriceChanges
            }
            time_rule_updater.updateManualTimeRuleForCategory(category, json.dumps(manual_time_rule_data))
        if ruleType == "Seasonality":
            manual_seasonality_rule_data = {
                "active": True,  
                "durationInYears": duration,
                "priceMax": priceMaximum,
                "priceMin": priceMinimum,
                "timeZone": timezone,
                "seasonalPriceChanges": seasonalPriceChanges
            }
            season_rule_updater.updateManualSeasonalityRuleForCategory(category, json.dumps(manual_seasonality_rule_data))
        return jsonify({'message': 'rule created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/clear_rules', methods=['POST'])
def clear_rules():
    try:
        #data from client
        data = request.json 
        print("Received data from client:", data, flush=True)
        category = data.get('category')
        print("Category:", category, flush=True)
        # Restore default rules for the specified category
        time_rule_updated = time_rule_updater.restoreTimeRuleDefaultsForCategory(category)
        season_rule_updated = season_rule_updater.restoreSeasonalityRuleDefaultsForCategory(category)
        # Check if rules were successfully updated
        if time_rule_updated and season_rule_updated:
            print("Rules cleared successfully.", flush=True)
            return jsonify({'message': 'Rules cleared successfully'}), 200
        else:
            print("Failed to clear rules.", flush=True)
            return jsonify({'error': 'Failed to clear rules'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def hourly_update():
    print("Running manualHourlyPriceUpdate...")
    manual_hour_price_updater.manualHourlyPriceUpdate()
    print("manualHourlyPriceUpdate completed.") 

def seasonal_update():
    current_month = datetime.datetime.now().month
    if current_month == 12:  # December (Winter)
        print("Running manualSeasonalPriceUpdate...")
        manual_season_price_updater.manualSeasonalPriceUpdate('Winter')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 3:  # March (Spring)
        print("Running manualSeasonalPriceUpdate...")
        manual_season_price_updater.manualSeasonalPriceUpdate('Spring')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 6:  # June (Summer)
        print("Running manualSeasonalPriceUpdate...")
        manual_season_price_updater.manualSeasonalPriceUpdate('Summer')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 9:  # September (Fall)
        print("Running manualSeasonalPriceUpdate...")
        manual_season_price_updater.manualSeasonalPriceUpdate('Fall')
        print("manualSeasonalPriceUpdate completed.") 

def new_minute_update():
    print("A minute has passed")

scheduler.add_job(hourly_update, 'cron', hour='*')  
scheduler.add_job(new_minute_update, 'cron', minute='*')
scheduler.add_job(seasonal_update, 'cron', month='3,6,9,12', day='1', hour='0', minute='0')  

# Register the shutdown function
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)

