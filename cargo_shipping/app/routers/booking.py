from fastapi import APIRouter

from cargo_shipping.app.models import BookingRequest
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
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
factory = CargoFactory()
repository = cargo_repository.CargoRepository(db["booking"], factory)
service = BookingService(factory, repository)


@router.get("/", status_code=200)
async def get_booking(id: str):
    result = repository.find_by_tracking_id(id)
    return result.to_dict(result)


@router.post("/", status_code=201)
async def create_booking(request: BookingRequest):
    return service.execute(
        request.tracking_id, request.destination, request.deadline
    )
