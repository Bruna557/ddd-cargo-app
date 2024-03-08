from fastapi import APIRouter

from source.domain.model.cargo.cargo import Cargo

router = APIRouter(
    prefix="/booking",
    tags=["booking"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_booking(cargo: Cargo):
    pass
