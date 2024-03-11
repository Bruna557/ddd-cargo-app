"""Implement Location Repository"""

from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence.repositories.mongo_db_repository import (
    MongoDBRepository,
)


class LocationRepository:
    """
    Location Repository is an implementation of MongoDB Repository where Entity
    is Location
    """

    def find_by_code(self, code: str) -> Location:
        """Get a Location from the database filtering by code"""

        result = MongoDBRepository.get_by_key(self, "code", code)
        return Location(**result)

    def find_by_name(self, name: str) -> Location:
        """Get a Location from the database filtering by name"""

        result = MongoDBRepository.get_by_key(self, "name", name)
        return Location(**result)
