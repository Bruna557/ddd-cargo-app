from fastapi import APIRouter

from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.infrastructure.persistence import (
    cargo_repository,
    database,
)

router = APIRouter(
    prefix="/tracking",
    tags=["tracking"],
    responses={404: {"description": "Not found"}},
)


db = database.get_database()
cargo_factory = CargoFactory()
repository = cargo_repository.CargoRepository(db["booking"], cargo_factory)


@router.get("/")
async def get_location(tracking_id: str):
    cargo = repository.find_by_tracking_id(tracking_id)
    return {"location": cargo.delivery_history.current_location}


@router.get("/history")
async def get_history(tracking_id: str):
    cargo = repository.find_by_tracking_id(tracking_id)
    return {"history": cargo.delivery_history.handling_events}
