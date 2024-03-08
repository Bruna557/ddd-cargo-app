from datetime import time

from source.domain.model.base.entity import Entity
from source.domain.model.base.factory import Factory
from source.domain.model.carrier.carrier_movement import CarrierMovement
from source.domain.model.handling.handling_event import (
    HandlingActivity,
    HandlingEvent,
)


class HandlingEventFactory(Factory):
    def create(self, *args) -> Entity:
        return super().create(*args)

    def new_loading(
        self, loaded_onto: CarrierMovement, time_stamp: time
    ) -> HandlingEvent:
        result = HandlingEvent(HandlingActivity.LOADING, time_stamp)
        result.set_carrier_movement(loaded_onto)
        return result
