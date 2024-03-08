from datetime import time
from uuid import uuid4

from cargo_shipping.domain.model.base.entity import Entity
from cargo_shipping.domain.model.location.location import Location


class CarrierMovement(Entity):
    def __init__(
        self,
        departure_location: Location,
        arrival_location: Location,
        departure_time: time,
    ) -> None:
        Entity.__init__(self, str(uuid4()))
        self.departure_location = departure_location
        self.arrival_location = arrival_location
        self.departure_time = departure_time
        self.arrival_time = None

    def set_arrival_time(self, time_stamp: time) -> None:
        self.arrival_time = time_stamp
