"""Implement Carrier Movement Repository"""

from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence.repositories.mongo_db_repository import (
    MongoDBRepository,
)


class CarrierMovementRepository(MongoDBRepository):
    """
    Carrier Movement Repository is an implementation of MongoDB Repository
    where Entity is Carrier Movement
    """

    def find_by_id(self, entity_id: str) -> CarrierMovement:
        """
        Get a Carrier Movement from the database filtering by entity_id
        """

        result = MongoDBRepository.get_by_key(self, "entity_id", entity_id)
        return CarrierMovement(**result)

    def find_by_tracking_id(self, tracking_id: str) -> CarrierMovement:
        """
        Get a Carrier Movement from the database filtering by the tracking_id
        of the associated Cargo
        """

        result = MongoDBRepository.get_by_key(self, "tracking_id", tracking_id)
        return CarrierMovement(**result)

    def find_by_departure_arrival(
        self, departure: Location, arrival: Location
    ) -> CarrierMovement:
        """
        Get a Carrier Movement from the database filtering by departure and
        arrival locations
        """

        result = self.collection.find_one(
            {"departure_location": departure, "arrival_location": arrival},
            {"_id": 0},
        )
        return CarrierMovement(**result)

    def save(self, entity: CarrierMovement) -> None:
        return MongoDBRepository.save(self, entity)
