from fastapi import APIRouter

from source.domain.model.cargo.cargo import Cargo

router = APIRouter(
    prefix="/tracking",
    tags=["tracking"],
    responses={404: {"description": "Not found"}},
)


@router.get("/location")
async def get_location(cargo: Cargo):
    pass


@router.get("/history")
async def get_history(cargo: Cargo):
    pass
