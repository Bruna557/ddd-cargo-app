from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.infrastructure.persistence.repository import Repository


class CargoRepository(Repository):
    def find_by_id(self, id: str) -> Cargo:
        pass

    def find_by_tracking_id(self, tracking_id: str) -> Cargo:
        pass

    def find_by_client_id(self, client_id: str) -> Cargo:
        pass

    def save(self, cargo: Cargo) -> None:
        pass
