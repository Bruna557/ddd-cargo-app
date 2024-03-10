from fastapi import APIRouter

from cargo_shipping.app.models import BookingRequest
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.booking_service import BookingService
from cargo_shipping.infrastructure.persistence import (
    cargo_repository,
    database,
)

router = APIRouter(
    prefix="/booking",
    tags=["booking"],
    responses={404: {"description": "Not found"}},
)


db = database.get_database()
handling_event_factory = HandlingEventFactory()
cargo_factory = CargoFactory(handling_event_factory)
repository = cargo_repository.CargoRepository(db["booking"], cargo_factory)
service = BookingService(cargo_factory, repository)


@router.get("/", status_code=200)
async def get_booking(id: str):
    result = repository.find_by_tracking_id(id)
    return result.to_dict()


@router.post("/", status_code=201)
async def create_booking(request: BookingRequest):
    return service.execute(
        request.tracking_id,
        Location(request.destination.code, request.destination.name),
        request.deadline,
    )
