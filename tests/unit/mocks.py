from collections import defaultdict

from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.infrastructure.persistence.repository import Repository


class FakeCargoRepository(Repository):
    def __init__(self) -> None:
        self.cargos = defaultdict()

    def save(self, cargo: Cargo) -> None:
        self.cargos[cargo.id] = cargo

    def get_by_key(self, key: str) -> CarrierMovement:
        return self.cargos[key]

    def find_by_tracking_id(self, tracking_id: str) -> Cargo:
        return self.get_by_key(tracking_id)


class FakeCarrierMovementRepository(Repository):
    def __init__(self) -> None:
        self.carrier_movements = defaultdict()

    def save(self, carrier_movement: CarrierMovement) -> None:
        self.carrier_movements[carrier_movement.id] = carrier_movement

    def get_by_key(self, key: str) -> CarrierMovement:
        return self.carrier_movements[key]

    # helper for testing
    def get_all(self) -> defaultdict:
        return list(self.carrier_movements.values())
