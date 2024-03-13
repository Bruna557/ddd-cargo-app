"""API methods for adding handling events."""

from fastapi import APIRouter, Depends

from cargo_shipping.api.dependencies import (
    get_loading_service,
    get_unloading_service,
)
from cargo_shipping.api.models import HandlingEventRequest
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingEventTypes,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.loading_service import (
    LoadingService,
    LoadingServiceConfig,
)
from cargo_shipping.domain.services.unloading_service import (
    UnloadingService,
    UnloadingServiceConfig,
)

router = APIRouter(
    prefix="/handling",
    tags=["handling"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", status_code=201)
async def add_handling_event(
    request: HandlingEventRequest,
    loading_service: LoadingService = Depends(get_loading_service),
    unloading_service: UnloadingService = Depends(get_unloading_service),
):
    """Add handling event (either LOADING or UNLOADING)."""

    match request.event_type:
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
