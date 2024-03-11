"""Implement Cargo Repository"""

from typing import List

from pymongo.collection import Collection

from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.infrastructure.persistence.repositories.mongo_db_repository import (
    MongoDBRepository,
)


class CargoRepository(MongoDBRepository):
    """
    Cargo Repository is an implementation of MongoDB Repository where Entity is
    Cargo Aggregate Root
    """

    def __init__(self, collection: Collection, factory: CargoFactory):
        MongoDBRepository.__init__(self, collection)
        self.factory = factory

    def find_by_tracking_id(self, tracking_id: str) -> Cargo:
        """Get a Cargo from the database filtering by tracking_id"""

        result = MongoDBRepository.get_by_key(self, "tracking_id", tracking_id)
        return self.factory.create_from_dict(result)

    def find_by_client_id(self, client_id: str) -> List[Cargo]:
        """Get all Cargs from the database that match the provided client_id"""
        result = MongoDBRepository.get_by_key(self, "client_id", client_id)
        return self.factory.create_from_dict(result)

    def save(self, entity: Cargo) -> None:
        return MongoDBRepository.save(self, entity)
