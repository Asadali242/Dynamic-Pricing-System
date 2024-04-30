from flask import Blueprint, jsonify, request
from services import hybrid_price_updater

suggestion_price_update_blueprint = Blueprint('suggestion_price_update_blueprint', __name__)
@suggestion_price_update_blueprint.route('/suggestion_price_update', methods=['POST'])
def update_price():
    recommendation = request.json.get('recommendation')
    hybrid_price_updater.updateSingleItemPrice(recommendation)
    return jsonify({'success': True, 'message': 'Price updated successfully'})


