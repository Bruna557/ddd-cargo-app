"""API methods for getting tracking information."""

from fastapi import APIRouter, Depends

from cargo_shipping.api.dependencies import get_cargo_repository
from cargo_shipping.infrastructure.persistence.repositories.cargo_repository import (
    CargoRepository,
)

router = APIRouter(
    prefix="/tracking",
    tags=["tracking"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_location(
    tracking_id: str,
    repository: CargoRepository = Depends(get_cargo_repository),
):
    """Get the current location of a cargo."""

    cargo = repository.find_by_tracking_id(tracking_id)
    return {"location": cargo.delivery_history.current_location}


@router.get("/history")
async def get_history(
    tracking_id: str,
    repository: CargoRepository = Depends(get_cargo_repository),
):
    """Get the history of handling events of a cargo."""

    cargo = repository.find_by_tracking_id(tracking_id)
    return {
        "history": [
            handling_event.to_dict()
            for handling_event in cargo.delivery_history.handling_events
        ]
    }
