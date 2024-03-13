"""End-to-end tests."""

from fastapi.testclient import TestClient

from cargo_shipping.api.dependencies import (
    get_loading_service,
    get_unloading_service,
)
from cargo_shipping.api.main import app
from cargo_shipping.domain.model.cargo.cargo_factory import (
    CargoFactory,
    CargoFactoryConfig,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingEventTypes,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from cargo_shipping.domain.services.loading_service import LoadingService
from cargo_shipping.domain.services.unloading_service import UnloadingService
from tests import utils
from tests.e2e.mocks import FakeCargoRepository, FakeCarrierMovementRepository

handling_event_factory = HandlingEventFactory()
cargo_factory = CargoFactory(handling_event_factory)
cargo_repository = FakeCargoRepository()
carrier_movement_repository = FakeCarrierMovementRepository()


def override_get_loading_service():
    """Override get_loading_service."""

    return LoadingService(
        handling_event_factory, cargo_repository, carrier_movement_repository
    )


def override_get_unloading_service():
    """Override get_unloading_service."""

    return UnloadingService(
        handling_event_factory, cargo_repository, carrier_movement_repository
    )


app.dependency_overrides[get_loading_service] = override_get_loading_service
app.dependency_overrides[get_unloading_service] = (
    override_get_unloading_service
)
client = TestClient(app)


class TestHandlingApi:
    """Test Handling API."""

    def test_add_handling_event(self):
        """Test add_handling_event method."""

        # 1. Prepare
        tracking_id = utils.random_string()
        departure_location_code = utils.random_string()
        departure_location_name = utils.random_string()
        arrival_location_code = utils.random_string()
        arrival_location_name = utils.random_string()
        time_stamp = utils.random_datetime()
        event_type = HandlingEventTypes.LOADING
        cargo = cargo_factory.create(
            CargoFactoryConfig(
                tracking_id,
                Location(utils.random_string(), utils.random_string()),
                utils.random_datetime(),
            )
        )
        cargo_repository.save(cargo)

        # 2. Execute
        response = client.post(
            "/handling",
            headers={"Content-Type": "application/json"},
            json={
                "tracking_id": tracking_id,
                "departure_location": {
                    "code": departure_location_code,
                    "name": departure_location_name,
                },
                "arrival_location": {
                    "code": arrival_location_code,
                    "name": arrival_location_name,
                },
                "time_stamp": time_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                "event_type": event_type,
            },
        )

        # 3. Assert
        cargo = cargo_repository.find_by_tracking_id(tracking_id)
        assert response.status_code == 201
        assert (
            cargo.delivery_history.handling_events[0].event_type == event_type
        )
        assert (
            cargo.delivery_history.handling_events[0].completion_time
            == time_stamp
        )
        assert (
            cargo.delivery_history.handling_events[
                0
            ].carrier_movement.departure_location.code
            == departure_location_code
        )
        assert (
            cargo.delivery_history.handling_events[
                0
            ].carrier_movement.departure_location.name
            == departure_location_name
        )
        assert (
            cargo.delivery_history.handling_events[
                0
            ].carrier_movement.arrival_location.code
            == arrival_location_code
        )
        assert (
            cargo.delivery_history.handling_events[
                0
            ].carrier_movement.arrival_location.name
            == arrival_location_name
        )
        assert (
            cargo.delivery_history.handling_events[
                0
            ].carrier_movement.departure_time
            == time_stamp
        )
        assert (
            cargo.delivery_history.handling_events[
                0
            ].carrier_movement.arrival_time
            is None
        )
