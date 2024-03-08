from typing import List
from uuid import uuid4

from source.domain.model.base.entity import Entity
from source.domain.model.carrier.carrier_movement import CarrierMovement
from source.domain.model.handling.handling_event import HandlingEvent
from source.domain.model.location.location import Location


class DeliveryHistory(Entity):
    def __init__(self) -> None:
        Entity.__init__(self, str(uuid4()))
        # TODO: fix
        # self.handling_events = List[HandlingEvent]
        self.handling_events = []

    def add(self, handling_event: HandlingEvent) -> None:
        self.handling_events.append(handling_event)

    @property
    def get_latest_carrier_movement(self) -> CarrierMovement:
        last_handling_event: HandlingEvent = self.handling_events[-1]
        return last_handling_event.carrier_movement

    @property
    def current_location(self) -> Location:
        latest_carrier_movement = self.get_latest_carrier_movement
        if latest_carrier_movement.arrival_time:
            return latest_carrier_movement.arrival_location
        return latest_carrier_movement.departure_location
