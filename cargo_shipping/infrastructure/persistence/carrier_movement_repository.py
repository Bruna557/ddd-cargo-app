from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence.repository import (
    MongoDBRepository,
)


class CarrierMovementRepository(MongoDBRepository):
    def find_by_id(self, id: str) -> CarrierMovement:
        result = MongoDBRepository.get_by_key(self, "id", id)
        return CarrierMovement(**result)

    def find_by_tracking_id(self, tracking_id: str) -> CarrierMovement:
        result = MongoDBRepository.get_by_key(self, "tracking_id", tracking_id)
        return CarrierMovement(**result)

    def find_by_from_to(
        self, from_: Location, to: Location
    ) -> CarrierMovement:
        result = self.collection.find_one(
            {"from": from_, "to": to}, {"_id": 0}
        )
        return CarrierMovement(**result)

    def save(self, carrier_movement: CarrierMovement) -> None:
        return MongoDBRepository.save(self, carrier_movement)
