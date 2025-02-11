from flask import Blueprint, request, jsonify
from services import (
    create_customer, get_customer, create_order, get_orders_by_customer,
    orders_by_billing_zip, orders_by_shipping_zip, in_store_order_times, top_customers
)

crm_routes = Blueprint("crm", __name__)
order_routes = Blueprint("orders", __name__)
analytics_routes = Blueprint("analytics", __name__)

### Customer Endpoints ###
@crm_routes.route("/customers", methods=["POST"])
def create_customer_route():
    data = request.get_json()
    response, status = create_customer(data)
    return jsonify(response), status

@crm_routes.route("/customers", methods=["GET"])
def get_customer_route():
    email = request.args.get("email")
    phone = request.args.get("phone")
    response, status = get_customer(email, phone)
    return jsonify(response), status

### Order Endpoints ###
@order_routes.route("/orders", methods=["POST"])
def create_order_route():
    data = request.get_json()
    response, status = create_order(data)
    return jsonify(response), status

@order_routes.route("/orders", methods=["GET"])
def get_orders_by_customer_route():
    email = request.args.get("email")
    phone = request.args.get("phone")
    response, status = get_orders_by_customer(email, phone)
    return jsonify(response), status

### Analytics Endpoints ###
@analytics_routes.route("/analytics/orders_by_billing_zip", methods=["GET"])
def orders_by_billing_zip_route():
    response, status = orders_by_billing_zip(request.args.get("order", "desc"))
    return jsonify(response), status

@analytics_routes.route("/analytics/orders_by_shipping_zip", methods=["GET"])
def orders_by_shipping_zip_route():
    response, status = orders_by_shipping_zip(request.args.get("order", "asc"))
    return jsonify(response), status

@analytics_routes.route("/analytics/in_store_order_times", methods=["GET"])
def in_store_order_times_route():
    response, status = in_store_order_times()
    return jsonify(response), status

@analytics_routes.route("/analytics/top_5_customers", methods=["GET"])
def top_customers_route():
    response, status = top_customers()
    return jsonify(response), status
