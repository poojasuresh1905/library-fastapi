import os
from pymongo import MongoClient

def get_db():
    # Read connection details from environment variables
    MONGO_URI = os.environ.get("MONGO_URI")
    DB_NAME = os.environ.get("DB_NAME")

    if not MONGO_URI:
        raise ValueError("❌ Missing MONGO_URI environment variable.")
    if not DB_NAME:
        raise ValueError("❌ Missing DB_NAME environment variable.")

    # Initialize MongoDB client
    client = MongoClient(MONGO_URI)

    # Return database instance
    return client[DB_NAME]
