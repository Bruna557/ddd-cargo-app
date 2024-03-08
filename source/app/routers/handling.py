from fastapi import APIRouter

from source.domain.model.handling.handling_event import HandlingEvent

router = APIRouter(
    prefix="/handling",
    tags=["handling"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def add_handling_event(event: HandlingEvent):
    pass
