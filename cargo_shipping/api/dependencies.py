"""Define functions that return the API's dependencies."""

from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.services.loading_service import LoadingService
from cargo_shipping.domain.services.unloading_service import UnloadingService
from cargo_shipping.infrastructure.persistence import database
from cargo_shipping.infrastructure.persistence.repositories.cargo_repository import (
    CargoRepository,
)
from cargo_shipping.infrastructure.persistence.repositories.carrier_movement_repository import (
    CarrierMovementRepository,
)


def get_db() -> database:
    """Get database."""

    return database.get_database()


def get_handling_event_factory() -> HandlingEventFactory:
    """Returns a Handling Event Factory."""

    return HandlingEventFactory


def get_cargo_factory() -> CargoFactory:
    """Returns a Cargo Factory."""

    handling_event_factory = get_handling_event_factory()
    return CargoFactory(handling_event_factory)


def get_cargo_repository() -> CargoRepository:
    """Returns a Cargo Repository."""

    db = get_db()
    cargo_factory = get_cargo_factory()
    return CargoRepository(db["booking"], cargo_factory)


def get_carrier_movement_repository() -> CargoRepository:
    """Returns a Carrier Movement Repository."""

    db = get_db()
    return CarrierMovementRepository(db["carrier_movements"])


def get_loading_service():
    """Get Loading Service."""

    handling_event_factory = get_handling_event_factory()
    cargo_repository = get_cargo_repository()
    carrier_movement_repository = get_carrier_movement_repository()

    return LoadingService(
        handling_event_factory, cargo_repository, carrier_movement_repository
    )


def get_unloading_service():
    """Get Unloading Service."""

    handling_event_factory = get_handling_event_factory()
    cargo_repository = get_cargo_repository()
    carrier_movement_repository = get_carrier_movement_repository()
    return UnloadingService(
        handling_event_factory, cargo_repository, carrier_movement_repository
    )
