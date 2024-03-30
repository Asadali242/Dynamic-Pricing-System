from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import logging
from database import getItemsByCategory, getItems, updateManualTimeRuleForCategory
import json

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
        return jsonify({'message': 'Time rule created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
