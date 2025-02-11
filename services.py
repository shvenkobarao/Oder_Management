from models import (
    get_customer_by_email_or_phone, create_customer_record, create_order_record, get_orders_by_customer_id,
    get_orders_grouped_by_zip, get_in_store_order_times, get_top_customers
)
import datetime

### Customer ###
def create_customer(data):
    """Ensure unique customer creation by email/phone."""
    if get_customer_by_email_or_phone(data["email"], data["phone"]):
        return {"error": "Customer already exists"}, 400

    customer_data = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "phone": data["phone"],
    }
    customer_id = create_customer_record(customer_data)
    return {"message": "Customer created", "customer_id": str(customer_id)}, 201

def get_customer(email=None, phone=None):
    """Retrieve customer by email or phone."""
    customer = get_customer_by_email_or_phone(email, phone)
    if not customer:
        return {"error": "Customer not found"}, 404
    return customer, 200

### Order ###
def create_order(data):
    """Ensure customer exists before creating an order."""
    customer = get_customer_by_email_or_phone(email=data["customer_email"])
    if not customer:
        return {"error": "Customer not found"}, 404

    order_data = {
        "customer_id": customer["_id"],
        "order_date": datetime.datetime.utcnow(),
        "billing_address": data["billing_address"],
        "shipping_addresses": data.get("shipping_addresses", []),
        "in_store": data["in_store"],
        "store_address": data.get("store_address")
    }
    order_id = create_order_record(order_data)
    return {"message": "Order created", "order_id": str(order_id)}, 201

def get_orders_by_customer(email=None, phone=None):
    """Retrieve orders linked to a customer."""
    customer = get_customer_by_email_or_phone(email, phone)
    if not customer:
        return {"error": "Customer not found"}, 404

    orders = get_orders_by_customer_id(customer["_id"])
    return {"orders": orders}, 200

### Analytics ###
def orders_by_billing_zip(order="desc"):
    return get_orders_grouped_by_zip("billing_address", order), 200

def orders_by_shipping_zip(order="asc"):
    return get_orders_grouped_by_zip("shipping_addresses", order), 200

def in_store_order_times():
    return get_in_store_order_times(), 200

def top_customers():
    return get_top_customers(), 200
