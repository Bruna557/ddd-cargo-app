import abc

from cargo_shipping.domain.model.base.entity import Entity


class Repository(abc.ABC):
    @abc.abstractmethod
    def save(self, entity: Entity) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_key(self, key: str) -> Entity:
        raise NotImplementedError()


class MongoDBRepository(Repository):
    def __init__(self, collection):
        self.collection = collection

    def save(self, entity: Entity) -> None:
        self.collection.insert_one(entity)

    def get_by_key(self, key: str) -> Entity:
        return self.collection.find_one({f"{key}": key})
