from datetime import time

from source.domain.model.carrier.carrier_movement import CarrierMovement
from source.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from source.domain.model.location.location import Location
from source.infrastructure.persistence.cargo_repository import CargoRepository
from source.infrastructure.persistence.carrier_movement_repository import (
    CarrierMovementRepository,
)


class LoadingService:
    def __init__(
        self,
        handling_event_factory: HandlingEventFactory,
        cargo_repository: CargoRepository,
        carrier_movement_repository: CarrierMovementRepository,
    ) -> None:
        self.handling_event_factory = handling_event_factory
        self.cargo_repository = cargo_repository
        self.carrier_movement_repository = carrier_movement_repository

    def execute(
        self,
        tracking_id: str,
        departure_location: Location,
        arrival_location: Location,
        time_stamp: time,
    ) -> None:

        cargo = self.cargo_repository.find_by_tracking_id(tracking_id)
        carrier_movement = CarrierMovement(
            departure_location, arrival_location, time_stamp
        )
        handling_event = self.handling_event_factory.new_loading(
            carrier_movement, time_stamp
        )
        cargo.delivery_history.add(handling_event)
        self.cargo_repository.save(cargo)
        self.carrier_movement_repository.save(carrier_movement)
