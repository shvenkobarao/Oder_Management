from flask import Flask
from routes import order_routes, crm_routes, analytics_routes
from database import initialize_db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

initialize_db(app)

app.register_blueprint(order_routes)
app.register_blueprint(crm_routes)
app.register_blueprint(analytics_routes)


if __name__ == "__main__":
    app.run(debug=True)
