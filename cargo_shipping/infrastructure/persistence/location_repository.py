from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence.repository import (
    MongoDBRepository,
)


class LocationRepository:
    def find_by_code(self, code: str) -> Location:
        result = MongoDBRepository.get_by_key(self, "code", code)
        return Location(**result)

    def find_by_name(self, name: str) -> Location:
        result = MongoDBRepository.get_by_key(self, "name", name)
        return Location(**result)
