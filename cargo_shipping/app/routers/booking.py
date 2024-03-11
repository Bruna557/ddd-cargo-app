"""API methods for getting and creating cargo bookings."""

from fastapi import APIRouter

from cargo_shipping.app.models import BookingRequest
from cargo_shipping.domain.model.cargo.cargo_factory import (
    CargoFactory,
    CargoFactoryConfig,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence import database
from cargo_shipping.infrastructure.persistence.repositories import (
    cargo_repository,
)

router = APIRouter(
    prefix="/booking",
    tags=["booking"],
    responses={404: {"description": "Not found"}},
)


db = database.get_database()
handling_event_factory = HandlingEventFactory()
cargo_factory = CargoFactory(handling_event_factory)
cargo_repository_ = cargo_repository.CargoRepository(
    db["booking"], cargo_factory
)


@router.get("/", status_code=200)
async def get_booking(tracking_id: str):
    """Get a cargo booking by id."""

    result = cargo_repository_.find_by_tracking_id(tracking_id)
    return result.to_dict()


@router.post("/", status_code=201)
async def create_booking(request: BookingRequest):
    """Create a cargo booking."""
    destination = Location(request.destination.code, request.destination.name)
    booking = cargo_factory.create(
        CargoFactoryConfig(request.tracking_id, destination, request.deadline)
    )
    return cargo_repository_.save(booking)
