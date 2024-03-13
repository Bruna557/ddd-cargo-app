"""Implement Unloading Service."""

from dataclasses import dataclass
from datetime import datetime

from cargo_shipping.domain.model.base.domain_service import (
    DomainService,
    DomainServiceConfig,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingEventTypes,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
    HandlingEventFactoryConfig,
)
from cargo_shipping.infrastructure.persistence.repositories.cargo_repository import (
    CargoRepository,
)
from cargo_shipping.infrastructure.persistence.repositories.carrier_movement_repository import (
    CarrierMovementRepository,
)


@dataclass
class UnloadingServiceConfig(DomainServiceConfig):
    """
    This class encapsulates the values needed for the Unoading Service to
    execute a an UNLOADING Handling Event and Carrier Movement:
    - entity_id: a Cargo's id used to track the Cargo
    - time_stamp: date and time when the Event ocurred
    """

    entity_id: str
    time_stamp: datetime


class UnloadingService(DomainService):
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

    def execute(self, config: UnloadingServiceConfig) -> None:
        cargo = self.cargo_repository.find_by_tracking_id(config.entity_id)
        carrier_movement = cargo.delivery_history.latest_carrier_movement
        handling_event = self.handling_event_factory.create(
            HandlingEventFactoryConfig(
                carrier_movement,
                config.time_stamp,
                HandlingEventTypes.UNLOADING,
            )
        )
        carrier_movement.set_arrival_time(config.time_stamp)
        cargo.delivery_history.add(handling_event)
        self.cargo_repository.save(cargo)
        self.carrier_movement_repository.save(carrier_movement)
