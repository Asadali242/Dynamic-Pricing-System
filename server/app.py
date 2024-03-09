from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import logging

app = Flask(__name__)
CORS(app)

@app.route('/save_rule', methods=['POST'])
def save_rule():
    data = request.json  #contains the data sent from the client
    #access the data 
    print(data, flush=True)  # print received data in the console
    return jsonify({'message': 'Rule saved successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)