# Order Management API
This is a Flask + MongoDB based Order Management API that provides Customer Management, Order Processing, and Analytics capabilities.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Customers API](#customers-api)
  - [Orders API](#orders-api)
  - [Analytics API](#analytics-api)
- [Example API Usage](#example-api-usage)
- [Running Tests](#running-tests)

---

## Features
Customer Management - Uniq Email/Phone
Order Management (Multiple Orders Per Customer)
Address Handling (Billing & Multiple Shipping Addresses)
Order Analytics (Top Customers, Sales by ZIP, Peak Order Times) 

---

## Installation
### Prerequisites
- Python
- MongoDB
- Flask
- Docker (Optional)

### Steps
1. Clone the repository
   git clone https://github.com/shvenkobarao/Oder_Management.git
   cd order-management-api

2. Create a virtual environment
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Set up MongoDB connection (config.py)
  MONGO_URI = "mongodb://localhost:27017/order_management"

5. Run the application
   python run.py

6. Access API at
   http://127.0.0.1:5000

---

## API Endpoints
### Customers API
Create a new customer
`/customers` | `POST`

Get customer by email
`/customers?email={email}` | `GET`

Get customer by phone
`/customers?phone={phone}` | `GET`

### Orders API
Create a new order 
`/orders` | `POST`

Get order history for a customer
`/orders?email={email}` | `GET`

### Analytics API
Orders aggregated by billing ZIP: 
`/analytics/orders_by_billing_zip?order=desc` | `GET`

Orders aggregated by shipping ZIP: 
`/analytics/orders_by_shipping_zip?order=asc` | `GET`

Top 5 hours of day with most in-store orders
`/analytics/in_store_order_times` | `GET`

Top 5 customers with most orders
`/analytics/top_5_customers` | `GET`

---

## Running Tests
pytest -v tests/

---

## Example API Usage
### Create a Customer
curl -X POST http://127.0.0.1:5000/customers -H "Content-Type: application/json" -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "1234567890",
  "billing_address": {
    "address_line1": "123 Main St",
    "address_line2": "Apt 4B",
    "city": "New York",
    "state": "NY",
    "zip": "10001"
  }
}'

### Get Customer by Email
curl -X GET "http://127.0.0.1:5000/customers?email=john.doe@example.com"

### Create an Order
curl -X POST http://127.0.0.1:5000/orders -H "Content-Type: application/json" -d '{
  "customer_email": "john.doe@example.com",
  "items": [{"name": "Sofa", "price": 499.99}],
  "in_store": false,
  "billing_address": {
    "address_line1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip": "10001"
  },
  "shipping_addresses": [
    {
      "address_line1": "500 Oak St",
      "city": "San Francisco",
      "state": "CA",
      "zip": "94105"
    }
  ]
}'

### Get Orders by Customer
curl -X GET "http://127.0.0.1:5000/orders?email=john.doe@example.com"


### Get Order History for a Customer
curl -X GET "http://127.0.0.1:5000/orders?email=john.doe@example.com"


### ### Get Order History for a Customer with No Orders (Should Return Empty List)
curl -X GET "http://127.0.0.1:5000/orders?email=empty@example.com"


### Get Orders Aggregated by Billing ZIP (Descending Order)
curl -X GET "http://127.0.0.1:5000/analytics/orders_by_billing_zip?order=desc"

### Get Orders Aggregated by Shipping ZIP (Ascending Order)
curl -X GET "http://127.0.0.1:5000/analytics/orders_by_shipping_zip?order=asc"

### Get In-Store Order Times Distribution
curl -X GET "http://127.0.0.1:5000/analytics/in_store_order_times"


### Get Top 5 Customers by Number of Orders
curl -X GET "http://127.0.0.1:5000/analytics/top_5_customers"

