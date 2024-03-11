"""Handling Event Entity Implementation."""

from datetime import datetime
from enum import Enum

from cargo_shipping.domain.model.base.entity import Entity
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)


class HandlingEventTypes(str, Enum):
    """Possible Handling Event types."""

    LOADING = "LOADING"
    UNLOADING = "UNLOADING"
    DELIVERING = "DELIVERING"


class HandlingEvent(Entity):
    """
    A Handling Events is an Entity that represents Events (like loading,
    unloading and delivering) that happened to a Cargo.
    """

    def __init__(
        self,
        entity_id: str,
        event_type: HandlingEventTypes,
        completion_time: datetime,
    ) -> None:
        Entity.__init__(self, entity_id)
        self.event_type = event_type
        self.completion_time = completion_time
        self.carrier_movement = None

    def set_carrier_movement(self, carrier_movement: CarrierMovement) -> None:
        """Add a Carrier Movement to the Handling Event."""

        self.carrier_movement = carrier_movement

    def to_dict(self) -> dict:
        return {
            "entity_id": self.entity_id,
            "event_type": self.event_type,
            "completion_time": self.completion_time,
            "carrier_movement": self.carrier_movement.to_dict(),
        }
