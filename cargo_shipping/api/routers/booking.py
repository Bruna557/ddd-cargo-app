"""API methods for getting and creating cargo bookings."""

from fastapi import APIRouter, Depends

from cargo_shipping.api.dependencies import (
    get_cargo_factory,
    get_cargo_repository,
)
from cargo_shipping.api.models import BookingRequest
from cargo_shipping.domain.model.cargo.cargo_factory import (
    CargoFactory,
    CargoFactoryConfig,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.infrastructure.persistence.repositories.cargo_repository import (
    CargoRepository,
)

router = APIRouter(
    prefix="/booking",
    tags=["booking"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=200)
async def get_booking(
    tracking_id: str,
    repository: CargoRepository = Depends(get_cargo_repository),
):
    """Get a cargo booking by id."""

    result = repository.find_by_tracking_id(tracking_id)
    return result.to_dict()


@router.post("/", status_code=201)
async def create_booking(
    request: BookingRequest,
    factory: CargoFactory = Depends(get_cargo_factory),
    repository: CargoRepository = Depends(get_cargo_repository),
):
    """Create a cargo booking."""

    destination = Location(request.destination.code, request.destination.name)
    booking = factory.create(
        CargoFactoryConfig(request.tracking_id, destination, request.deadline)
    )
    return repository.save(booking)
