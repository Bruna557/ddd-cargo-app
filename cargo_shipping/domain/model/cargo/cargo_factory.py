from datetime import datetime

from cargo_shipping.domain.model.base.factory import Factory
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
)
from cargo_shipping.domain.model.location.location import Location


class CargoFactory(Factory):
    def create(
        self, id: str, destination: Location, deadline: datetime
    ) -> Cargo:
        cargo = Cargo(id)
        cargo.delivery_specification = DeliverySpecification(
            destination, deadline
        )
        return cargo

    def create_from_dict(self, d: dict):
        cargo = Cargo(d["id"])
        cargo.delivery_specification = DeliverySpecification(
            Location(
                d["delivery_specification"]["destination"]["name"],
                d["delivery_specification"]["destination"]["code"],
            ),
            d["delivery_specification"]["deadline"],
        )
        delivery_history = DeliveryHistory(d["delivery_history"]["id"])
        # TODO: inject dependency
        handling_event_factory = HandlingEventFactory()
        for handling_event in d["delivery_history"]["handling_events"]:
            carrier_movement = CarrierMovement(
                Location(
                    handling_event["carrier_movement"]["departure_location"][
                        "name"
                    ],
                    handling_event["carrier_movement"]["departure_location"][
                        "code"
                    ],
                ),
                Location(
                    handling_event["carrier_movement"]["arrival_location"][
                        "name"
                    ],
                    handling_event["carrier_movement"]["arrival_location"][
                        "code"
                    ],
                ),
                handling_event["carrier_movement"]["departure_time"],
                handling_event["carrier_movement"]["id"],
            )
            carrier_movement.set_arrival_time(
                handling_event["carrier_movement"]["arrival_time"]
            )
            delivery_history.add(
                handling_event_factory.create(
                    carrier_movement,
                    handling_event["completion_time"],
                    handling_event["type"],
                )
            )
        cargo.delivery_history = delivery_history
        return cargo
