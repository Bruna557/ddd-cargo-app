from datetime import datetime

from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.booking_service import BookingService
from tests.unit.mocks import FakeCargoRepository


class TestBookingService:
    def test_execute_success(self):
        """
        1. Prepare
        """
        # instantiate classes
        cargo_factory = CargoFactory()
        cargo_repository = FakeCargoRepository()
        booking_service = BookingService(cargo_factory, cargo_repository)

        # declare variables
        tracking_id = "TEST_ID"
        destination = Location("TEST_LOCATION", "TEST_CODE")
        deadline = datetime.today().strftime("%Y-%m-%d")

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
