from flask import Blueprint, jsonify, request
from services import price_change_history_getter, database_helpers

price_change_history_blueprint = Blueprint('price_change_history_blueprint', __name__)
@price_change_history_blueprint.route('/price_change_history', methods=['POST'])
def price_history():
    try:
        #name = request.json.get('name')
        #itemID = database_helpers.fetchItemIdByName(name)
        itemID = request.json.get('id') 
        price_history = price_change_history_getter.getPriceChangeHistoryForItem(itemID)
        return jsonify({'success': True, 'price_history': price_history})
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'success': False, 'error': error_message}), 500