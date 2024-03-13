"""Implement MongoDB Repository"""

from pymongo.collection import Collection

from cargo_shipping.domain.model.base.entity import Entity
from cargo_shipping.domain.model.base.repository import Repository


class MongoDBRepository(Repository):
    """
    MongoDB Repository abstracts away storage details of a MongoDB database
    """

    def __init__(self, collection: Collection):
        self.collection = collection

    def save(self, entity: Entity) -> None:
        self.collection.update_one(
            {"entity_id": entity.entity_id},
            {"$set": entity.to_dict()},
            upsert=True,
        )

    def get_by_key(self, key_name: str, key: str) -> dict:
        return self.collection.find_one({key_name: key}, {"_id": 0})
