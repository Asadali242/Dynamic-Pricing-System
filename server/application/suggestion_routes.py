from flask import Blueprint, jsonify
import datetime
from decimal import Decimal
from services import hybrid_hour_suggester


suggestion_blueprint = Blueprint('suggestion_blueprint', __name__)

@suggestion_blueprint.route('/get_recommendations')
def get_recommendations():
    current_time = datetime.datetime.now().hour
    suggestions = hybrid_hour_suggester.suggest_price_change(current_time)
    converted_suggestions = convert_decimals_to_float(suggestions)
    return jsonify(converted_suggestions)

def convert_decimals_to_float(obj):
    if isinstance(obj, dict):
        return {key: convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals_to_float(element) for element in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj