from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import logging
from database import getItemsByCategory, getItems, updateManualTimeRuleForCategory, updateManualSeasonalityRuleForCategory, manualHourlyPriceUpdate
import json
import schedule
import time

app = Flask(__name__)
CORS(app)

@app.route('/items_by_category', methods=['GET'])
def items_by_category():
    try:
        category = request.args.get('category')
        items = getItemsByCategory(category)
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/items_by_alphabet', methods=['GET'])
def items_by_alphabet():
    try:
        limit = request.args.get('limit', default=20, type=int)
        items = getItems(limit)
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
            updateManualTimeRuleForCategory(category, json.dumps(manual_time_rule_data))
        if ruleType == "Seasonality":
            manual_seasonality_rule_data = {
                "active": True,  
                "durationInYears": duration,
                "priceMax": priceMaximum,
                "priceMin": priceMinimum,
                "timeZone": timezone,
                "seasonalPriceChanges": seasonalPriceChanges
            }
            updateManualSeasonalityRuleForCategory(category, json.dumps(manual_seasonality_rule_data))
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
        updateManualTimeRuleForCategory(category, json.dumps(default_time_rule_data))
        updateManualSeasonalityRuleForCategory(category, json.dumps(default_seasonality_rule_data))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

   
def hourly_update():
    print("Running manualHourlyPriceUpdate...")
    manualHourlyPriceUpdate()
    print("manualHourlyPriceUpdate completed.") 

schedule.every().hour.at(":00").do(hourly_update)
while True:
    schedule.run_pending()
    time.sleep(60) 

if __name__ == '__main__':
    app.run(debug=True, port=5000)
