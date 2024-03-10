from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.booking_service import BookingService
from tests import utils
from tests.unit.mocks import FakeCargoRepository


class TestBookingService:
    def test_execute_success(self):
        """
        1. Prepare
        """
        cargo_factory = CargoFactory(HandlingEventFactory())
        cargo_repository = FakeCargoRepository()
        booking_service = BookingService(cargo_factory, cargo_repository)

        tracking_id = utils.random_string()
        destination = Location(utils.random_string(), utils.random_string())
        deadline = utils.random_datetime()

        """
        2. Execute
        """
        booking_service.execute(tracking_id, destination, deadline)

        """
        3. Assert
        """
        byproduct_cargo = cargo_repository.find_by_tracking_id(tracking_id)
        assert byproduct_cargo.id == tracking_id
        assert (
            byproduct_cargo.delivery_specification.destination == destination
        )
        assert byproduct_cargo.delivery_specification.deadline == deadline
