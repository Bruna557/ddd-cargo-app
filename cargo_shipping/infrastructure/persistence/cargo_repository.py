from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.infrastructure.persistence.repository import (
    MongoDBRepository,
)


class CargoRepository(MongoDBRepository):
    def find_by_id(self, id: str) -> Cargo:
        return MongoDBRepository.get_by_key(id)

    def find_by_tracking_id(self, tracking_id: str) -> Cargo:
        return self.find_by_id(tracking_id)

    def find_by_client_id(self, client_id: str) -> Cargo:
        return MongoDBRepository.get_by_key(client_id)

    def save(self, cargo: Cargo) -> None:
        return MongoDBRepository.save(cargo)
