from datetime import datetime

from cargo_shipping.domain.model.base.value_object import ValueObject
from cargo_shipping.domain.model.location.location import Location


class DeliverySpecification(ValueObject):
    def __init__(self, destination: Location, deadline: datetime) -> None:
        self.destination = destination
        self.deadline = deadline
