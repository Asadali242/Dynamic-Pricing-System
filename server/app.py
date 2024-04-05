from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import logging
import database
import json
import schedule
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import datetime

app = Flask(__name__)
CORS(app)

scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/items_by_category', methods=['GET'])
def items_by_category():
    try:
        category = request.args.get('category')
        items = database.getItemsByCategory(category)
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/items_by_alphabet', methods=['GET'])
def items_by_alphabet():
    try:
        limit = request.args.get('limit', default=20, type=int)
        items = database.getItems(limit)
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
            database.updateManualTimeRuleForCategory(category, json.dumps(manual_time_rule_data))
        if ruleType == "Seasonality":
            manual_seasonality_rule_data = {
                "active": True,  
                "durationInYears": duration,
                "priceMax": priceMaximum,
                "priceMin": priceMinimum,
                "timeZone": timezone,
                "seasonalPriceChanges": seasonalPriceChanges
            }
            database.updateManualSeasonalityRuleForCategory(category, json.dumps(manual_seasonality_rule_data))
        return jsonify({'message': 'rule created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/clear_rules', methods=['POST'])
def clear_rules():
    try:
        #data from client
        data = request.json 
        print(data, flush=True)
        category = data.get('category')
        default_time_rule_data = {
                "active": False,  
                "durationInDays": None,
                "priceMax": None,
                "priceMin": None,
                "timeZone": "",
                "hourlyPriceChanges": {}
            }
        default_seasonality_rule_data = {
                "active": False,  
                "durationInYears": None,
                "priceMax": None,
                "priceMin": None,
                "timeZone": "",
                "seasonalPriceChanges": {}
            }
        database.updateManualTimeRuleForCategory(category, json.dumps(default_time_rule_data))
        database.updateManualSeasonalityRuleForCategory(category, json.dumps(default_seasonality_rule_data))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def hourly_update():
    print("Running manualHourlyPriceUpdate...")
    database.manualHourlyPriceUpdate()
    print("manualHourlyPriceUpdate completed.") 

def seasonal_update():
    current_month = datetime.datetime.now().month
    if current_month == 12:  # December (Winter)
        print("Running manualSeasonalPriceUpdate...")
        database.manualSeasonalPriceUpdate('Winter')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 3:  # March (Spring)
        print("Running manualSeasonalPriceUpdate...")
        database.manualSeasonalPriceUpdate('Spring')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 6:  # June (Summer)
        print("Running manualSeasonalPriceUpdate...")
        database.manualSeasonalPriceUpdate('Summer')
        print("manualSeasonalPriceUpdate completed.") 
    elif current_month == 9:  # September (Fall)
        print("Running manualSeasonalPriceUpdate...")
        database.manualSeasonalPriceUpdate('Fall')
        print("manualSeasonalPriceUpdate completed.") 

def new_minute_update():
    print("A minute has passed")

scheduler.add_job(database.hourly_update, 'cron', hour='*')  
scheduler.add_job(database.new_minute_update, 'cron', minute='*')
scheduler.add_job(database.seasonal_update, 'cron', month='3,6,9,12', day='1', hour='0', minute='0')  

# Register the shutdown function
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)

