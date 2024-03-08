import uuid
from datetime import time
from enum import Enum

from source.domain.model.base.entity import Entity
from source.domain.model.carrier.carrier_movement import CarrierMovement


class HandlingActivity(Enum):
    LOADING = "LOADING"
    UNLOADING = "UNLOADING"
    RECEIVED = "RECEIVED"


class HandlingEvent(Entity):
    def __init__(
        self,
        type: HandlingActivity,
        completion_time: time,
    ) -> None:
        Entity.__init__(self, str(uuid.uuid4()))
        self.type = type
        self.completion_time = completion_time
        self.carrier_movement = None

    def set_carrier_movement(self, carrier_movement: CarrierMovement) -> None:
        self.carrier_movement = carrier_movement
