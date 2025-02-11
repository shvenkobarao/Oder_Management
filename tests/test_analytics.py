import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_orders_by_billing_zip(client):
    response = client.get("/analytics/orders_by_billing_zip?order=desc")
    assert response.status_code == 200, f"Unexpected response: {response.json}"
    assert isinstance(response.json, list)

def test_orders_by_shipping_zip(client):
    response = client.get("/analytics/orders_by_shipping_zip?order=asc")
    assert response.status_code == 200, f"Unexpected response: {response.json}"
    assert isinstance(response.json, list)

def test_in_store_order_times(client):
    response = client.get("/analytics/in_store_order_times")
    assert response.status_code == 200, f"Unexpected response: {response.json}"
    assert isinstance(response.json, list)

def test_top_5_customers(client):
    response = client.get("/analytics/top_5_customers")
    assert response.status_code == 200, f"Unexpected response: {response.json}"
    assert isinstance(response.json, list)
