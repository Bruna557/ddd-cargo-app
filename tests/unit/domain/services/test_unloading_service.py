from datetime import datetime

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
from cargo_shipping.domain.services.unloading_service import UnLoadingService
from tests.unit.mocks import FakeCargoRepository, FakeCarrierMovementRepository


class TestUnLoadingService:
    def test_execute_success(self):
        """
        1. Prepare
        """
        # instantiate classes
        handling_event_factory = HandlingEventFactory()
        cargo_repository = FakeCargoRepository()
        carrier_movement_repository = FakeCarrierMovementRepository()
        unloading_service = UnLoadingService(
            handling_event_factory,
            cargo_repository,
            carrier_movement_repository,
        )

        # create cargo booking
        tracking_id = "TEST_ID"
        destination = Location("TEST_DEST", "DEST_CODE")
        deadline = datetime.now()
        cargo = CargoFactory().create(tracking_id, destination, deadline)

        # create loading carrier movement
        departure_location = Location("TEST_DEPARTURE", "DEPARTURE_CODE")
        arrival_location = Location("TEST_ARRIVAL", "ARRIVAL_CODE")
        departure_time = datetime.now()
        arrival_time = datetime.now()
        carrier_movement = CarrierMovement(
            departure_location, arrival_location, departure_time
        )
        carrier_movement_repository.save(carrier_movement)

        # add loading handling event
        handling_event = handling_event_factory.create(
            carrier_movement, departure_time, HandlingActivity.LOADING
        )
        cargo.delivery_history.add(handling_event)
        cargo_repository.save(cargo)

        """
        2. Execute
        """
        unloading_service.execute(tracking_id, arrival_time)

        """
        3. Assert
        """
        byproduct_handling_event = cargo.delivery_history.handling_events[1]
        assert byproduct_handling_event.type == HandlingActivity.UNLOADING
        assert byproduct_handling_event.completion_time == arrival_time
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
            == departure_time
        )
        assert (
            byproduct_handling_event.carrier_movement.arrival_time
            == arrival_time
        )
        assert carrier_movement.arrival_time == arrival_time
