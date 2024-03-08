from fastapi import APIRouter

from cargo_shipping.domain.model.cargo.cargo import Cargo
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
collection = db["booking"]
repository = cargo_repository.CargoRepository(collection)


@router.post("/", status_code=201)
async def create_booking(cargo: Cargo):
    return repository.save(cargo)
