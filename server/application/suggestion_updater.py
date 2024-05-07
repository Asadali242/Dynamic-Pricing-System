import datetime
from services import hybrid_hour_suggester, hybrid_season_suggester
from flask_socketio import emit
from decimal import Decimal

#for initiating the suggestions if there is a fetch when the suggestions are empty
#only updates the global variable
def hourly_suggestion_updater(suggestions):
    current_time = datetime.datetime.now().hour
    suggestions_data = hybrid_hour_suggester.suggest_price_change(current_time) 
    suggestions.update(suggestions_data)  # Update the global suggestions variable
    print("Sent the following Suggestions to the browser: ", suggestions)

#updates the global variable and emits to the client so it will update without needing to fetch
def hourly_suggestion_emitter(socketio, suggestions):
    current_time = datetime.datetime.now().hour
    suggestions_data = hybrid_hour_suggester.suggest_price_change(current_time) 
    suggestions.update(suggestions_data)  # Update the global suggestions variable
    converted_suggestions = convert_decimals_to_float(suggestions_data)
    socketio.emit('hourly_suggestions', converted_suggestions)
    print("hourly emitter Updated hourly suggestions for the hour")
    print("Suggestions: ", suggestions)

def seasonal_suggestion_updater(suggestions):
    suggestions_data = hybrid_season_suggester.suggest_price_change(1) 
    #suggestions.update(suggestions_data)
    for category, items in suggestions_data.items():
        if category in suggestions:
            suggestions[category].extend(items)
        else:
            suggestions[category] = items
    print("Sent the following  Suggestions to the browser: ", suggestions)

    
def seasonal_suggestion_emitter(socketio, suggestions):
    suggestions_data = hybrid_season_suggester.suggest_price_change(1) 
    #suggestions.update(suggestions_data)
    for category, items in suggestions_data.items():
        if category in suggestions:
            suggestions[category].extend(items)
        else:
            suggestions[category] = items
    print("seasonalemitter Sent the following Suggestions to the browser: ", suggestions)

    converted_suggestions = convert_decimals_to_float(suggestions_data)
    socketio.emit('seasonal_suggestions', converted_suggestions)
    print("Updated seasonal suggestions for the hour")
    print("Suggestions: ", suggestions)




def convert_decimals_to_float(obj):
    if isinstance(obj, dict):
        return {key: convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals_to_float(element) for element in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj