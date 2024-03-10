from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingActivity,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.loading_service import LoadingService
from tests import utils
from tests.unit.mocks import FakeCargoRepository, FakeCarrierMovementRepository


class TestLoadingService:
    def test_execute_success(self):
        """
        1. Prepare
        """
        handling_event_factory = HandlingEventFactory()
        cargo_repository = FakeCargoRepository()
        carrier_movement_repository = FakeCarrierMovementRepository()
        loading_service = LoadingService(
            handling_event_factory,
            cargo_repository,
            carrier_movement_repository,
        )

        # create cargo booking
        tracking_id = utils.random_string()
        destination = Location(utils.random_string(), utils.random_string())
        deadline = utils.random_datetime()
        cargo = CargoFactory(HandlingEventFactory()).create(
            tracking_id, destination, deadline
        )
        cargo_repository.save(cargo)

        departure_location = Location(
            utils.random_string(), utils.random_string()
        )
        arrival_location = Location(
            utils.random_string(), utils.random_string()
        )
        time_stamp = utils.random_datetime()

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
