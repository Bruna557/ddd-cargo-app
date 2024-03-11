"""Handling Event Factory implementation."""

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from cargo_shipping.domain.model.base.factory import Factory, FactoryConfig
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingEvent,
    HandlingEventTypes,
)
from cargo_shipping.domain.model.location.location import Location


@dataclass
class HandlingEventFactoryConfig(FactoryConfig):
    """
    This class encapsulates the values needed for the Handling Event Factory to
    create a Handling Event:
    - entity_id: Entity identity
    - loaded_onto: a Carrier Movement that represents where the Cargo was
    loaded
    - time_stamp: the date and time when the Event occurred
    - handling_event_type: the type of the Event
    """

    loaded_onto: CarrierMovement
    time_stamp: datetime
    handling_event_type: HandlingEventTypes
    entity_id: str = uuid4()


class HandlingEventFactory(Factory):
    """This class is responsible for creating Handling Event Entities."""

    def create(self, config: HandlingEventFactoryConfig) -> HandlingEvent:
        result = HandlingEvent(
            config.entity_id, config.handling_event_type, config.time_stamp
        )
        result.set_carrier_movement(config.loaded_onto)
        return result

    def create_from_dict(self, d: dict) -> HandlingEvent:
        return self.create(
            HandlingEventFactoryConfig(
                CarrierMovement(
                    Location(
                        d["carrier_movement"]["departure_location"]["code"],
                        d["carrier_movement"]["departure_location"]["name"],
                    ),
                    Location(
                        d["carrier_movement"]["arrival_location"]["code"],
                        d["carrier_movement"]["arrival_location"]["name"],
                    ),
                    d["carrier_movement"]["departure_time"],
                    d["carrier_movement"]["id"],
                    d["carrier_movement"]["arrival_time"],
                ),
                d["completion_time"],
                d["event_type"],
                d["entity_id"],
            )
        )
