"""Delivery History Entity (included in the Cargo Aggregate) implementation."""

from typing import List
from uuid import uuid4

from cargo_shipping.domain.model.base.entity import Entity
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event import HandlingEvent
from cargo_shipping.domain.model.location.location import Location


class DeliveryHistory(Entity):
    """
    Delivery History is an Entity that stores all the Handling Events
    associated with a Cargo.
    """

    def __init__(self, entity_id: str = str(uuid4())) -> None:
        Entity.__init__(self, entity_id)
        self.handling_events: List[HandlingEvent] = []

    def add(self, handling_event: HandlingEvent) -> None:
        """Add a Handling Event to the history."""

        self.handling_events.append(handling_event)

    @property
    def latest_carrier_movement(self) -> CarrierMovement:
        """The most recent Carrier Moviment in the Delivery History."""

        last_handling_event: HandlingEvent = self.handling_events[-1]
        return last_handling_event.carrier_movement

    @property
    def current_location(self) -> Location:
        """A Cargo's curren location based on the latest Carrier Movement."""

        latest_carrier_movement = self.latest_carrier_movement
        if latest_carrier_movement.arrival_time:
            return latest_carrier_movement.arrival_location
        return latest_carrier_movement.departure_location

    def to_dict(self) -> dict:
        dict_ = {"entity_id": self.entity_id, "handling_events": []}
        for handling_event in self.handling_events:
            dict_["handling_events"].append(handling_event.to_dict())
        return dict_
