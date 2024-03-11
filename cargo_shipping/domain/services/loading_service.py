"""Loading Service implementation."""

from dataclasses import dataclass
from datetime import datetime

from cargo_shipping.domain.model.base.domain_service import (
    DomainService,
    DomainServiceConfig,
)
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
    HandlingEventFactoryConfig,
    HandlingEventTypes,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence.repositories.cargo_repository import (
    CargoRepository,
)
from cargo_shipping.infrastructure.persistence.repositories.carrier_movement_repository import (
    CarrierMovementRepository,
)


@dataclass
class LoadingServiceConfig(DomainServiceConfig):
    """
    This class encapsulates the values needed for the Loading Service to
    execute a a LOADING Handling Event and Carrier Movement:
    - tracking_id: a Cargo's id used to track the Cargo
    - departure_location: where the Cargo departured from
    - arrival_location: where the cargo arrived to
    - time_stamp: date and time when the Event ocurred
    """

    tracking_id: str
    departure_location: Location
    arrival_location: Location
    time_stamp: datetime


class LoadingService(DomainService):
    """
    Loading Service is a Domain Service responsible to execute a LOADING
    Handling Event for a determined Cargo.
    """

    def __init__(
        self,
        handling_event_factory: HandlingEventFactory,
        cargo_repository: CargoRepository,
        carrier_movement_repository: CarrierMovementRepository,
    ) -> None:
        self.handling_event_factory = handling_event_factory
        self.cargo_repository = cargo_repository
        self.carrier_movement_repository = carrier_movement_repository

    def execute(self, config: DomainServiceConfig) -> None:
        cargo = self.cargo_repository.find_by_tracking_id(config.tracking_id)
        carrier_movement = CarrierMovement(
            config.departure_location,
            config.arrival_location,
            config.time_stamp,
        )
        handling_event = self.handling_event_factory.create(
            HandlingEventFactoryConfig(
                carrier_movement, config.time_stamp, HandlingEventTypes.LOADING
            )
        )
        cargo.delivery_history.add(handling_event)
        self.cargo_repository.save(cargo)
        self.carrier_movement_repository.save(carrier_movement)
