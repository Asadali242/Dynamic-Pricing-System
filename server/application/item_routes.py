from flask import Blueprint, jsonify, request
from services import item_retriever

item_blueprint = Blueprint('item_blueprint', __name__)

@item_blueprint.route('/items_by_category', methods=['GET'])
def items_by_category():
    try:
        category = request.args.get('category')
        items = item_retriever.getItemsByCategory(category)
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@item_blueprint.route('/items_by_alphabet', methods=['GET'])
def items_by_alphabet():
    try:
        limit = request.args.get('limit', default=20, type=int)
        items = item_retriever.getItems(limit)
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500