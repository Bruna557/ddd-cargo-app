"""Mocks for unit tests."""

from collections import defaultdict

from mongomock import MongoClient

from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.infrastructure.persistence.repositories.cargo_repository import (
    CargoRepository,
)
from cargo_shipping.infrastructure.persistence.repositories.carrier_movement_repository import (
    CarrierMovementRepository,
)


class FakeEventHandlingFactory(HandlingEventFactory):
    """Fake Event Handling Factory for testing."""


class FakeCargoFactory(CargoFactory):
    """Fake Cargo Factory for testing."""

    def __init__(self):
        CargoFactory.__init__(self, FakeEventHandlingFactory())


class FakeCargoRepository(CargoRepository):
    """Fake Cargo Repository for testing."""

    def __init__(self) -> None:
        CargoRepository.__init__(
            self, MongoClient().mydb.mycollection, FakeCargoFactory()
        )
        self.cargos = defaultdict()

    def save(self, entity: Cargo) -> None:
        self.cargos[entity.entity_id] = entity

    def get_by_key(self, key_name: str, key: str) -> CarrierMovement:
        return self.cargos[key]

    def find_by_tracking_id(self, tracking_id: str) -> Cargo:
        return self.get_by_key("", tracking_id)


class FakeCarrierMovementRepository(CarrierMovementRepository):
    """Fake Carrier Movement for testing."""

    def __init__(self) -> None:
        CarrierMovementRepository.__init__(
            self, MongoClient().mydb.mycollection
        )
        self.carrier_movements = defaultdict()

    def save(self, entity: CarrierMovement) -> None:
        self.carrier_movements[entity.entity_id] = entity

    def get_by_key(self, key_name: str, key: str) -> CarrierMovement:
        return self.carrier_movements[key]

    def get_all(self) -> defaultdict:
        """Helper for testing. Return all carrier movements."""

        return list(self.carrier_movements.values())
