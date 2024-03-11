"""Get database connection"""

import os

from pymongo import MongoClient


def get_database():
    """Get a connection to the MongoDB database"""

    user = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "")
    password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "")
    connection_string = f"mongodb://{user}:{password}@mongodb:27017"

    client = MongoClient(connection_string)

    return client["cargo_shipping"]
