from fastapi import APIRouter

from cargo_shipping.app.models import HandlingEventRequest
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingActivity,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.loading_service import LoadingService
from cargo_shipping.domain.services.unloading_service import UnLoadingService
from cargo_shipping.infrastructure.persistence import (
    cargo_repository,
    carrier_movement_repository,
    database,
)

router = APIRouter(
    prefix="/handling",
    tags=["handling"],
    responses={404: {"description": "Not found"}},
)


db = database.get_database()
handling_event_factory = HandlingEventFactory()
cargo_factory = CargoFactory(handling_event_factory)
cargo_repository_ = cargo_repository.CargoRepository(
    db["booking"], cargo_factory
)
carrier_movement_repository_ = (
    carrier_movement_repository.CarrierMovementRepository(
        db["carrier_movements"]
    )
)
loading_service = LoadingService(
    handling_event_factory, cargo_repository_, carrier_movement_repository_
)
unloading_service = UnLoadingService(
    handling_event_factory, cargo_repository_, carrier_movement_repository_
)


@router.post("/", status_code=201)
async def add_handling_event(request: HandlingEventRequest):
    match request.handling_activity:
        case HandlingActivity.LOADING:
            return loading_service.execute(
                request.tracking_id,
                Location(
                    request.departure_location.code,
                    request.departure_location.name,
                ),
                Location(
                    request.arrival_location.code,
                    request.arrival_location.name,
                ),
                request.time_stamp,
            )
        case HandlingActivity.UNLOADING:
            return unloading_service.execute(
                request.tracking_id, request.time_stamp
            )
