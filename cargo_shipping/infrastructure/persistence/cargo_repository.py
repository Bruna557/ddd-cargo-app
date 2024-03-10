from pymongo.collection import Collection

from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.infrastructure.persistence.mongo_db_repository import (
    MongoDBRepository,
)


class CargoRepository(MongoDBRepository):
    def __init__(self, collection: Collection, factory: CargoFactory):
        MongoDBRepository.__init__(self, collection)
        self.factory = factory

    def find_by_id(self, id: str) -> Cargo:
        result = MongoDBRepository.get_by_key(self, "id", id)
        return self.factory.create_from_dict(result)

    def find_by_tracking_id(self, tracking_id: str) -> Cargo:
        return self.find_by_id(tracking_id)

    def find_by_client_id(self, client_id: str) -> Cargo:
        result = MongoDBRepository.get_by_key(self, client_id)
        return self.factory.create_from_dict(result)

    def save(self, cargo: Cargo) -> None:
        return MongoDBRepository.save(self, cargo)
