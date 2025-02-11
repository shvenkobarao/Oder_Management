import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_order(client):
    # Create Customer
    client.post("/customers", json={
        "first_name": "Order",
        "last_name": "Tester",
        "email": "test.order@example.com",
        "phone": "9876543210"
    })

    # Create Order
    response = client.post("/orders", json={
        "customer_email": "test.order@example.com",
        "items": [{"name": "Chair", "price": 100.00}],
        "in_store": False,
        "billing_address": {
            "address_line1": "123 Test St",
            "city": "Los Angeles",
            "state": "CA",
            "zip": "90001"
        },
        "shipping_addresses": [
            {
                "address_line1": "456 Oak St",
                "city": "Austin",
                "state": "TX",
                "zip": "73301"
            },
            {
                "address_line1": "789 Main St",
                "city": "Irving",
                "state": "TX",
                "zip": "75038"
            }
        ]
    })
    assert response.status_code == 201, f"Unexpected response: {response.json}"

def test_create_order_customer_not_found(client):
    response = client.post("/orders", json={
        "customer_email": "notfound@example.com",
        "items": [{"name": "Table", "price": 199.99}],
        "in_store": True,
        "store_address_id": "store123"
    })
    assert response.status_code == 404, f"Unexpected response: {response.json}"

def test_get_order_history(client):
    response = client.get("/orders?email=test.order@example.com")
    assert response.status_code == 200, f"Unexpected response: {response.json}"
    assert isinstance(response.json["orders"], list)

def test_get_order_history_no_orders(client):
    response = client.get("/orders?email=empty@example.com")
    assert response.status_code == 200
    assert response.json["orders"] == []
