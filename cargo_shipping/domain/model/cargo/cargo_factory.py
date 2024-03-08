from datetime import time

from cargo_shipping.domain.model.base.entity import Entity
from cargo_shipping.domain.model.base.factory import Factory
from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.cargo.delivery_specification import (
    DeliverySpecification,
)
from cargo_shipping.domain.model.location.location import Location


class CargoFactory(Factory):

    def create(
        self, id: str, destination: Location, arrival_time: time
    ) -> Cargo:
        cargo = Cargo(id)
        cargo.delivery_specification = DeliverySpecification(
            destination, arrival_time
        )
        return cargo
