"""API methods for adding handling events."""

from fastapi import APIRouter

from cargo_shipping.app.models import HandlingEventRequest
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingEventTypes,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.loading_service import (
    LoadingService,
    LoadingServiceConfig,
)
from cargo_shipping.domain.services.unloading_service import (
    UnLoadingService,
    UnloadingServiceConfig,
)
from cargo_shipping.infrastructure.persistence import database
from cargo_shipping.infrastructure.persistence.repositories import (
    cargo_repository,
    carrier_movement_repository,
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
    """Add handling event (either LOADING or UNLOADING)."""

    match request.handling_event_type:
        case HandlingEventTypes.LOADING:
            return loading_service.execute(
                LoadingServiceConfig(
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
            )
        case HandlingEventTypes.UNLOADING:
            return unloading_service.execute(
                UnloadingServiceConfig(request.tracking_id, request.time_stamp)
            )
