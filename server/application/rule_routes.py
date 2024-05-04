import json
from flask import Blueprint, jsonify, request
from database_tests.database.time_rule_updater import TimeRuleUpdater
from database_tests.database.season_rule_updater import SeasonRuleUpdater
from services import time_rule_updater, season_rule_updater
from datetime import datetime

rule_blueprint = Blueprint('rule_blueprint', __name__)

@rule_blueprint.route('/create_rule', methods=['POST'])
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
        dateOfCreation = datetime.now()
        dateOfCreationStr = dateOfCreation.isoformat()
        
        if ruleType == "TimeOfDay":
            manual_time_rule_data = {
                "active": True,  
                "durationInDays": duration,
                "priceMax": priceMaximum,
                "priceMin": priceMinimum,
                "timeZone": timezone,
                "createDate" : dateOfCreationStr,
                "hourlyPriceChanges": hourlyPriceChanges,
            }
            time_rule_updater.updateManualTimeRuleForCategory(category, json.dumps(manual_time_rule_data))
        if ruleType == "Seasonality":
            manual_seasonality_rule_data = {
                "active": True,  
                "durationInYears": duration,
                "priceMax": priceMaximum,
                "priceMin": priceMinimum,
                "timeZone": timezone,
                "createDate" : dateOfCreationStr,
                "seasonalPriceChanges": seasonalPriceChanges,
            }
            season_rule_updater.updateManualSeasonalityRuleForCategory(category, json.dumps(manual_seasonality_rule_data))
        return jsonify({'message': 'rule created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@rule_blueprint.route('/clear_rules', methods=['POST'])
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