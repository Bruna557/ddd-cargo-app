from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence.mongo_db_repository import (
    MongoDBRepository,
)


class CarrierMovementRepository(MongoDBRepository):
    def find_by_id(self, id: str) -> CarrierMovement:
        result = MongoDBRepository.get_by_key(self, "id", id)
        return CarrierMovement(**result)

    def find_by_tracking_id(self, tracking_id: str) -> CarrierMovement:
        result = MongoDBRepository.get_by_key(self, "tracking_id", tracking_id)
        return CarrierMovement(**result)

    def find_by_departure_arrival(
        self, departure: Location, arrival: Location
    ) -> CarrierMovement:
        result = self.collection.find_one(
            {"departure_location": departure, "arrival_location": arrival},
            {"_id": 0},
        )
        return CarrierMovement(**result)

    def save(self, carrier_movement: CarrierMovement) -> None:
        return MongoDBRepository.save(self, carrier_movement)
