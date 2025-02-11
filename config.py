import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/order_management")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    TESTING = os.getenv("TESTING", "False").lower() in ("true", "1", "t")
