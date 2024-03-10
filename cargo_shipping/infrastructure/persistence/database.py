import os

from mongoengine import connect
from pymongo import MongoClient


def get_database():
    user = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "")
    password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "")
    CONNECTION_STRING = f"mongodb://{user}:{password}@mongodb:27017"

    client = connect(CONNECTION_STRING)

    return client["cargo_shipping"]
