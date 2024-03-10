from datetime import datetime
from uuid import uuid4

from cargo_shipping.domain.model.base.entity import Entity
from cargo_shipping.domain.model.location.location import Location


class CarrierMovement(Entity):
    def __init__(
        self,
        departure_location: Location,
        arrival_location: Location,
        departure_time: datetime,
        id: str = str(uuid4()),
        arrival_time: datetime | None = None,
    ) -> None:
        Entity.__init__(self, id)
        self.departure_location = departure_location
        self.arrival_location = arrival_location
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def set_arrival_time(self, time_stamp: datetime) -> None:
        self.arrival_time = time_stamp

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "departure_location": self.departure_location.to_dict(),
            "arrival_location": self.arrival_location.to_dict(),
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
        }
