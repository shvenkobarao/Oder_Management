import pytest
import json
from app import app

ORDERS_JSON_PATH = "/Users/sheelav/Downloads/Radiant-Graph_Data-Project/order_management/Test_data/orders.json"

@pytest.fixture
def client():
    """Set up test client for Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def load_orders():
    """Load orders from orders.json file."""
    try:
        with open(ORDERS_JSON_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to load orders.json: {e}")

def test_bulk_insert_orders(client):
    """Test inserting multiple orders from orders.json."""
    orders = load_orders()
    
    for order in orders:
        response = client.post("/orders", json=order)
        assert response.status_code in [201, 400], f"Unexpected response: {response.json}"
        if response.status_code == 400:
            print(f"Duplicate or invalid order skipped: {order}")

