from datetime import time

from source.domain.model.cargo.cargo_factory import CargoFactory
from source.domain.model.location.location import Location
from source.infrastructure.persistence.cargo_repository import CargoRepository


class BookingService:
    def __init__(
        self, factory: CargoFactory, repository: CargoRepository
    ) -> None:
        self.factory = factory
        self.repository = repository

    def execute(
        self, tracking_id: str, destination: Location, arrival_time: time
    ):
        cargo = self.factory.create(tracking_id, destination, arrival_time)
        cargo = self.repository.save(cargo)
