from datetime import time

from cargo_shipping.domain.model.base.value_object import ValueObject
from cargo_shipping.domain.model.location.location import Location


class DeliverySpecification(ValueObject):
    def __init__(self, destination: Location, arrival_time: time) -> None:
        self.destination = destination
        self.arrival_time = arrival_time
