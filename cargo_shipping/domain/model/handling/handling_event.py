import uuid
from datetime import datetime
from enum import Enum

from cargo_shipping.domain.model.base.entity import Entity
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)


class HandlingActivity(str, Enum):
    LOADING = "LOADING"
    UNLOADING = "UNLOADING"
    DELIVERED = "DELIVERED"


class HandlingEvent(Entity):
    def __init__(
        self,
        type: HandlingActivity,
        completion_time: datetime,
    ) -> None:
        Entity.__init__(self, str(uuid.uuid4()))
        self.type = type
        self.completion_time = completion_time
        self.carrier_movement = None

    def set_carrier_movement(self, carrier_movement: CarrierMovement) -> None:
        self.carrier_movement = carrier_movement

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "completion_time": self.completion_time,
            "carrier_movement": self.carrier_movement.to_dict(),
        }
