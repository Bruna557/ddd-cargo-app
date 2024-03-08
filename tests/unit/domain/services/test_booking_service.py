from collections import defaultdict
from datetime import datetime

from cargo_shipping.domain.model.base.entity import Entity
from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.booking_service import BookingService
from cargo_shipping.infrastructure.persistence.repository import Repository
from tests.unit.mocks import FakeCargoRepository


class TestBookingService:
    def test_execute_success(self):
        cargo_factory = CargoFactory()
        cargo_repository = FakeCargoRepository()
        booking_service = BookingService(cargo_factory, cargo_repository)
        tracking_id = "TEST_ID"
        destination = Location("TEST_LOCATION", "TEST_CODE")
        arrival_time = datetime.now()

        booking_service.execute(tracking_id, destination, arrival_time)

        created_cargo = cargo_repository.find_by_tracking_id(tracking_id)
        assert created_cargo.id == tracking_id
        assert created_cargo.delivery_specification.destination == destination
        assert (
            created_cargo.delivery_specification.arrival_time == arrival_time
        )
