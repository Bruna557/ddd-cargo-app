from collections import defaultdict
from datetime import datetime

from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingActivity,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.loading_service import LoadingService
from cargo_shipping.infrastructure.persistence.repository import Repository


class FakeCargoRepository(Repository):
    def __init__(self) -> None:
        self.cargos = defaultdict()

    def save(self, cargo: Cargo) -> None:
        self.cargos[cargo.id] = cargo

    def get_by_id(self, id: str) -> Cargo:
        return self.find_by_tracking_id(id)

    def find_by_tracking_id(self, tracking_id: str) -> Cargo:
        return self.cargos[tracking_id]


class FakeCarrierMovementRepository(Repository):
    def __init__(self) -> None:
        self.carrier_movements = defaultdict()

    def save(self, carrier_movement: CarrierMovement) -> None:
        self.carrier_movements[carrier_movement.id] = carrier_movement

    # helper for testing
    def get_all(self) -> defaultdict:
        return list(self.carrier_movements.values())

    def get_by_id(self, id: str) -> CarrierMovement:
        return self.carrier_movements[id]


class TestLoadingService:
    def test_execute_success(self):
        handling_event_factory = HandlingEventFactory()
        cargo_repository = FakeCargoRepository()
        carrier_movement_repository = FakeCarrierMovementRepository()
        loading_service = LoadingService(
            handling_event_factory,
            cargo_repository,
            carrier_movement_repository,
        )
        tracking_id = "TEST_ID"
        destination = Location("TEST_DEST", "DEST_CODE")
        arrival_time = datetime.now()
        cargo_repository.save(
            CargoFactory().create(tracking_id, destination, arrival_time)
        )
        departure_location = Location("TEST_DEPARTURE", "DEPARTURE_CODE")
        arrival_location = Location("TEST_ARRIVAL", "ARRIVAL_CODE")
        time_stamp = datetime.now()

        loading_service.execute(
            tracking_id, departure_location, arrival_location, time_stamp
        )

        cargo = cargo_repository.get_by_id(tracking_id)
        handling_event = cargo.delivery_history.handling_events[0]
        carrier_movement = carrier_movement_repository.get_all()[0]
        assert handling_event.type == HandlingActivity.LOADING
        assert handling_event.completion_time == time_stamp
        assert (
            handling_event.carrier_movement.departure_location
            == departure_location
        )
        assert (
            handling_event.carrier_movement.arrival_location
            == arrival_location
        )
        assert handling_event.carrier_movement.departure_time == time_stamp
        assert handling_event.carrier_movement.arrival_time is None
        assert carrier_movement.departure_location == departure_location
        assert carrier_movement.arrival_location == arrival_location
        assert carrier_movement.departure_time == time_stamp
