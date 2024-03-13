"""Cargo Factory implementation."""

from dataclasses import dataclass
from datetime import datetime

from cargo_shipping.domain.model.base.factory import Factory, FactoryConfig
from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.cargo.delivery_history import DeliveryHistory
from cargo_shipping.domain.model.cargo.delivery_specification import (
    DeliverySpecification,
)
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
    HandlingEventFactoryConfig,
)
from cargo_shipping.domain.model.location.location import Location


@dataclass
class CargoFactoryConfig(FactoryConfig):
    """
    This class encapsulates the values needed for the Cargo Factory to create a
    Cargo:
    - entity_id: a Cargo's id used to track the Cargo
    - destination: where the Cargo should be delivered to
    - deadline: the Cargo must be delivered before the deadline
    """

    entity_id: str
    destination: Location
    deadline: datetime


class CargoFactory(Factory):
    """This class is responsible for creating Cargos Aggregates."""

    def __init__(self, handling_event_factory: HandlingEventFactory):
        self.handling_event_factory = handling_event_factory

    def create(self, config: CargoFactoryConfig) -> Cargo:
        """This method creates a new Cargo aggregate."""

        cargo = Cargo(config.entity_id)
        cargo.delivery_specification = DeliverySpecification(
            config.destination, config.deadline
        )
        return cargo

    def create_from_dict(self, d: dict) -> Cargo:
        """This method rebuilds a Cargo from its dictionary representation."""

        cargo = self.create(
            CargoFactoryConfig(
                d["entity_id"],
                Location(
                    d["delivery_specification"]["destination"]["code"],
                    d["delivery_specification"]["destination"]["name"],
                ),
                d["delivery_specification"]["deadline"],
            )
        )

        delivery_history = DeliveryHistory(d["delivery_history"]["entity_id"])
        for handling_event in d["delivery_history"]["handling_events"]:
            carrier_movement = CarrierMovement(
                Location(
                    handling_event["carrier_movement"]["departure_location"][
                        "code"
                    ],
                    handling_event["carrier_movement"]["departure_location"][
                        "name"
                    ],
                ),
                Location(
                    handling_event["carrier_movement"]["arrival_location"][
                        "code"
                    ],
                    handling_event["carrier_movement"]["arrival_location"][
                        "name"
                    ],
                ),
                handling_event["carrier_movement"]["departure_time"],
                handling_event["carrier_movement"]["entity_id"],
            )
            carrier_movement.set_arrival_time(
                handling_event["carrier_movement"]["arrival_time"]
            )
            delivery_history.add(
                self.handling_event_factory.create(
                    HandlingEventFactoryConfig(
                        carrier_movement,
                        handling_event["completion_time"],
                        handling_event["event_type"],
                    )
                )
            )
        cargo.delivery_history = delivery_history

        return cargo
