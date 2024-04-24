import datetime
from services import hybrid_hour_suggester
from flask_socketio import emit
from decimal import Decimal

def hourly_suggestion_updater(socketio):
    current_time = datetime.datetime.now().hour
    suggestions = hybrid_hour_suggester.suggest_price_change(current_time) 
    #print("suggestions:", suggestions)
    converted_suggestions = convert_decimals_to_float(suggestions)
    
    socketio.emit('hourly_suggestions', converted_suggestions)
    print("Updated suggestions for the hour")

def convert_decimals_to_float(obj):
    if isinstance(obj, dict):
        return {key: convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals_to_float(element) for element in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj