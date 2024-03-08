from datetime import datetime

from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingActivity,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.loading_service import LoadingService
from tests.unit.mocks import FakeCargoRepository, FakeCarrierMovementRepository


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

        cargo = cargo_repository.find_by_tracking_id(tracking_id)
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
