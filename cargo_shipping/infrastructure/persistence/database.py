from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = (
        "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
    )

    client = MongoClient(CONNECTION_STRING)

    return client["cargo_shipping"]
