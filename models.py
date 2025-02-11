from database import mongo
from bson import ObjectId
import datetime

### Customers ###
def get_customer_by_email_or_phone(email=None, phone=None):
    """Retrieve customer by email or phone."""
    query = {"$or": [{"email": email}, {"phone": phone}]} if email or phone else {}
    return mongo.db.customers.find_one(query)

def create_customer_record(data):
    """Insert new customer record, ensuring uniqueness."""
    return mongo.db.customers.insert_one(data).inserted_id

### Orders ###
def create_order_record(order_data):
    """Insert a new order."""
    return mongo.db.orders.insert_one(order_data).inserted_id

def get_orders_by_customer_id(customer_id):
    """Retrieve all orders for a given customer."""
    return list(mongo.db.orders.find({"customer_id": ObjectId(customer_id)}))

### Analytics ###
def get_orders_grouped_by_zip(field_name, order):
    """Aggregate orders count by billing or shipping zip."""
    pipeline = [
        {"$unwind": f"${field_name}"},
        {"$group": {"_id": f"${field_name}.zip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1 if order == "desc" else 1}}
    ]
    return list(mongo.db.orders.aggregate(pipeline))

def get_in_store_order_times():
    """Analyze in-store purchase times."""
    pipeline = [
        {"$match": {"in_store": True}},
        {"$project": {"hour": {"$hour": "$order_date"}}},
        {"$group": {"_id": "$hour", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
        {"$project": {"hour": "$_id", "count": 1, "_id": 0}}
    ]
    return list(mongo.db.orders.aggregate(pipeline))

def get_top_customers():
    """Retrieve the top 5 customers by number of orders, including their email and phone."""
    pipeline = [
        {"$group": {"_id": "$customer_id", "order_count": {"$sum": 1}}},
        {"$sort": {"order_count": -1}},
        {"$limit": 5},
        {"$lookup": {  # Join with customers to get email/phone
            "from": "customers",
            "localField": "_id",
            "foreignField": "_id",
            "as": "customer_info"
        }},
        {"$unwind": "$customer_info"},
        {"$project": {
            "customer_id": "$_id",
            "order_count": 1,
            "email": "$customer_info.email",
            "phone": "$customer_info.phone"
        }}
    ]
    
    return list(mongo.db.orders.aggregate(pipeline))
