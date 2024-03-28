from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import logging
from database import getItemsByCategory, getItems

app = Flask(__name__)
CORS(app)

@app.route('/save_rule', methods=['POST'])
def save_rule():
    data = request.json  #contains the data sent from the client
    #access the data 
    print(data, flush=True)  # print received data in the console
    return jsonify({'message': 'Rule saved successfully'})

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
