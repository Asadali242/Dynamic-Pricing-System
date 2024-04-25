from flask import Flask, jsonify, request
from decimal import Decimal
from flask_socketio import SocketIO
from flask_cors import CORS
from item_routes import item_blueprint
from rule_routes import rule_blueprint
from scheduler import initialize_scheduler, register_jobs, register_shutdown
from rule_based_price_updates import hourly_update, seasonal_update, new_minute_update
from suggestion_updater import hourly_suggestion_updater, hourly_suggestion_emitter

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

app.register_blueprint(item_blueprint)
app.register_blueprint(rule_blueprint)

initialize_scheduler()
suggestions = {} 
register_jobs(hourly_update, new_minute_update, seasonal_update, hourly_suggestion_emitter, socketio, suggestions)
register_shutdown()


#fetches from the front end
@app.route('/get_recommendations')
def get_recommendations():
    if suggestions is None or not suggestions:
        hourly_suggestion_updater(suggestions)
    return jsonify(suggestions)

#when a recommendation is accepted or denied, we clear it from the server dict of suggestions
@app.route('/clear_recommendation', methods=['POST'])
def clear_recommendation():
    recommendation = request.json.get('recommendation')
    if recommendation:
        category = recommendation['category']
        item_name = recommendation['name']
        if category in suggestions:
            index_to_remove = None
            for index, item in enumerate(suggestions[category]):
                if item_name.strip() == item['name'].strip():
                    index_to_remove = index
                    break
            
            if index_to_remove is not None:
                del suggestions[category][index_to_remove]
                return jsonify({'success': True, 'message': 'Recommendation cleared.'}), 200
            else:
                return jsonify({'success': False, 'message': 'Recommendation not found.'}), 404
        else:
            return jsonify({'success': False, 'message': 'Category not found.'}), 404
    else:
        return jsonify({'success': False, 'message': 'No recommendation data received.'}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False)

