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
        """
        1. Prepare
        """
        # instantiate classes
        handling_event_factory = HandlingEventFactory()
        cargo_repository = FakeCargoRepository()
        carrier_movement_repository = FakeCarrierMovementRepository()
        loading_service = LoadingService(
            handling_event_factory,
            cargo_repository,
            carrier_movement_repository,
        )

        # create cargo booking
        tracking_id = "TEST_ID"
        destination = Location("TEST_DEST", "DEST_CODE")
        deadline = datetime.now()
        cargo = CargoFactory().create(tracking_id, destination, deadline)
        cargo_repository.save(cargo)

        # declare variables
        departure_location = Location("TEST_DEPARTURE", "DEPARTURE_CODE")
        arrival_location = Location("TEST_ARRIVAL", "ARRIVAL_CODE")
        time_stamp = datetime.now()

        """
        2. Execute
        """
        loading_service.execute(
            tracking_id, departure_location, arrival_location, time_stamp
        )

        """
        3. Assert
        """
        byproduct_handling_event = cargo.delivery_history.handling_events[0]
        byproduct_carrier_movement = carrier_movement_repository.get_all()[0]
        assert byproduct_handling_event.type == HandlingActivity.LOADING
        assert byproduct_handling_event.completion_time == time_stamp
        assert (
            byproduct_handling_event.carrier_movement.departure_location
            == departure_location
        )
        assert (
            byproduct_handling_event.carrier_movement.arrival_location
            == arrival_location
        )
        assert (
            byproduct_handling_event.carrier_movement.departure_time
            == time_stamp
        )
        assert byproduct_handling_event.carrier_movement.arrival_time is None
        assert (
            byproduct_carrier_movement.departure_location == departure_location
        )
        assert byproduct_carrier_movement.arrival_location == arrival_location
        assert byproduct_carrier_movement.departure_time == time_stamp
