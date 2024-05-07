from flask import Blueprint, jsonify, request
from services import total_units_sold_retriever
from services import total_sales_retriever



dashboard_statistic_blueprint = Blueprint('dashboard_statistic_blueprint', __name__)

@dashboard_statistic_blueprint.route('/get_total_units_sold', methods=['GET'])
def get_total_units_sold():
    print("entered get total units sold funtion")
    total_units_sold = total_units_sold_retriever.calculate_total_products_sold()
    print("calculated total equals ", total_units_sold)
    return jsonify(total_units_sold)

@dashboard_statistic_blueprint.route('/get_total_sales', methods=['GET'])
def get_total_sales():
    print("entered get total units sold funtion")
    total_sales = total_sales_retriever.calculate_total_sales()
    print("calculated total equals ", total_sales)
    return jsonify(total_sales)