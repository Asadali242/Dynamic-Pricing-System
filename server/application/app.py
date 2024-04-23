from flask import Flask
from flask_cors import CORS
from item_routes import item_blueprint
from rule_routes import rule_blueprint
from scheduler import initialize_scheduler, register_jobs, register_shutdown
from rule_based_price_updates import hourly_update, seasonal_update, new_minute_update

app = Flask(__name__)
CORS(app)

app.register_blueprint(item_blueprint)
app.register_blueprint(rule_blueprint)

initialize_scheduler()
register_jobs(hourly_update, new_minute_update, seasonal_update)
register_shutdown()

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)

