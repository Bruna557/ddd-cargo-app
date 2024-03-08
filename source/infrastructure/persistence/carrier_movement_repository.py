from ...domain.model.carrier.carrier_movement import CarrierMovement
from ...domain.model.location.location import Location


class CarrierMovementRepository:
    def find_by_schedule_id(self, schedule_id: str) -> CarrierMovement:
        pass

    def find_by_tracking_id(self, tracking_id: str) -> CarrierMovement:
        pass

    def find_by_from_to(
        self, from_: Location, to: Location
    ) -> CarrierMovement:
        pass

    def save(self, carrier_movement: CarrierMovement) -> None:
        pass
