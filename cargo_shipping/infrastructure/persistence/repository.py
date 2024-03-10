import abc
from typing import Dict

from pymongo.collection import Collection

from cargo_shipping.domain.model.base.entity import Entity


class Repository(abc.ABC):
    @abc.abstractmethod
    def save(self, entity: Entity) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_key(self, key_name: str, key: str) -> Dict:
        raise NotImplementedError()


class MongoDBRepository(Repository):
    def __init__(self, collection: Collection):
        self.collection = collection

    def save(self, entity: Entity) -> None:
        self.collection.update_one(
            {"id": entity.id}, {"$set": entity.to_dict(entity)}, upsert=True
        )

    def get_by_key(self, key_name: str, key: str) -> Dict:
        return self.collection.find_one({key_name: key}, {"_id": 0})
