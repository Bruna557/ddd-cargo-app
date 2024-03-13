"""Mocks for end_to_end tests."""

import mongomock

from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.infrastructure.persistence.repositories.cargo_repository import (
    CargoRepository,
)
from cargo_shipping.infrastructure.persistence.repositories.carrier_movement_repository import (
    CarrierMovementRepository,
)

mongo = mongomock.MongoClient()
test_db = mongo.test_db


class FakeCargoRepository(CargoRepository):
    """Fake Cargo Repository for testing."""

    def __init__(self) -> None:
        handling_event_factory = HandlingEventFactory()
        cargo_factory = CargoFactory(handling_event_factory)
        CargoRepository.__init__(self, test_db.bookings, cargo_factory)


class FakeCarrierMovementRepository(CarrierMovementRepository):
    """Fake Carrier Movement Repository for testing."""

    def __init__(self) -> None:
        CarrierMovementRepository.__init__(self, test_db.carrier_movements)
