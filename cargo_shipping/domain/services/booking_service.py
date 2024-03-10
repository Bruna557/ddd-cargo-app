from datetime import datetime

from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence.cargo_repository import (
    CargoRepository,
)


class BookingService:
    def __init__(
        self, factory: CargoFactory, repository: CargoRepository
    ) -> None:
        self.factory = factory
        self.repository = repository

    def execute(
        self, tracking_id: str, destination: Location, deadline: datetime
    ):
        cargo = self.factory.create(tracking_id, destination, deadline)
        cargo = self.repository.save(cargo)
