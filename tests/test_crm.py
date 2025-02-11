import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_customer(client):
    response = client.post("/customers", json={
        "first_name": "Alice",
        "last_name": "Doe",
        "email": "alice.doe@example.com",
        "phone": "1112223333"
    })
    assert response.status_code == 201, f"Unexpected response: {response.json}"

def test_duplicate_customer(client):
    response = client.post("/customers", json={
        "first_name": "Alice",
        "last_name": "Doe",
        "email": "alice.doe@example.com",
        "phone": "1112223333"
    })
    assert response.status_code == 400, f"Unexpected response: {response.json}"

def test_create_customer_missing_fields(client):
    response = client.post("/customers", json={
        "first_name": "Bob"
    })
    assert response.status_code == 400, f"Unexpected response: {response.json}"

def test_get_existing_customer(client):
    response = client.get("/customers?email=alice.doe@example.com")
    assert response.status_code == 200, f"Unexpected response: {response.json}"
    assert response.json["email"] == "alice.doe@example.com"

def test_get_non_existent_customer(client):
    response = client.get("/customers?email=nonexistent@example.com")
    assert response.status_code == 404, f"Unexpected response: {response.json}"
