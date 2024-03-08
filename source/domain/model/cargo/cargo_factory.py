from datetime import time

from source.domain.model.base.entity import Entity
from source.domain.model.base.factory import Factory
from source.domain.model.cargo.cargo import Cargo
from source.domain.model.cargo.delivery_specification import (
    DeliverySpecification,
)
from source.domain.model.location.location import Location


class CargoFactory(Factory):

    def create(
        self, id: str, destination: Location, arrival_time: time
    ) -> Cargo:
        cargo = Cargo(id)
        cargo.delivery_specification = DeliverySpecification(
            destination, arrival_time
        )
        return cargo
