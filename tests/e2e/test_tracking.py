"""End-to-end tests."""

from fastapi.testclient import TestClient

from cargo_shipping.api.dependencies import get_cargo_repository
from cargo_shipping.api.main import app
from cargo_shipping.domain.model.cargo.cargo_factory import (
    CargoFactory,
    CargoFactoryConfig,
)
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingEventTypes,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
    HandlingEventFactoryConfig,
)
from cargo_shipping.domain.model.location.location import Location
from tests import utils
from tests.e2e.mocks import FakeCargoRepository

handling_event_factory = HandlingEventFactory()
cargo_factory = CargoFactory(handling_event_factory)
cargo_repository = FakeCargoRepository()


def override_get_cargo_repository():
    """Override get_cargo_repository."""

    return cargo_repository


app.dependency_overrides[get_cargo_repository] = override_get_cargo_repository
client = TestClient(app)


class TestTrackingApi:
    """Test Tracking API."""

    def test_get_location(self):
        """Test get_location method."""

        # 1. Prepare
        tracking_id = utils.random_string()
        cargo = cargo_factory.create(
            CargoFactoryConfig(
                tracking_id,
                Location(utils.random_string(), utils.random_string()),
                utils.random_datetime(),
            )
        )
        departure_location_code = utils.random_string()
        departure_location_name = utils.random_string()
        arrival_location_code = utils.random_string()
        arrival_location_name = utils.random_string()
        loading_carrier_movement = CarrierMovement(
            Location(departure_location_code, departure_location_name),
            Location(arrival_location_code, arrival_location_name),
            utils.random_datetime(),
            utils.random_string(),
            utils.random_datetime(),
        )
        unloading_carrier_movement = CarrierMovement(
            Location(departure_location_code, departure_location_name),
            Location(arrival_location_code, arrival_location_name),
            utils.random_datetime(),
        )
        loading_handling_event = handling_event_factory.create(
            HandlingEventFactoryConfig(
                loading_carrier_movement,
                utils.random_datetime(),
                HandlingEventTypes.LOADING,
            ),
        )
        loading_handling_event.carrier_movement = loading_carrier_movement
        unloading_handling_event = handling_event_factory.create(
            HandlingEventFactoryConfig(
                unloading_carrier_movement,
                utils.random_datetime(),
                HandlingEventTypes.UNLOADING,
            )
        )
        unloading_handling_event.carrier_movement = unloading_carrier_movement
        cargo.delivery_history.add(loading_handling_event)
        cargo.delivery_history.add(unloading_handling_event)
        cargo_repository.save(cargo)

        # 2. Execute
        response = client.get(f"/tracking?tracking_id={tracking_id}")

        # 3. Assert
        response_body = response.json()
        assert response.status_code == 200
        assert response_body["location"]["code"] == departure_location_code
        assert response_body["location"]["name"] == departure_location_name

    def test_get_history(self):
        """Test get_history method."""

        # 1. Prepare
        tracking_id = utils.random_string()
        cargo = cargo_factory.create(
            CargoFactoryConfig(
                tracking_id,
                Location(utils.random_string(), utils.random_string()),
                utils.random_datetime(),
            )
        )
        loading_event_type = HandlingEventTypes.LOADING
        unloading_event_type = HandlingEventTypes.UNLOADING
        departure_location_code = utils.random_string()
        departure_location_name = utils.random_string()
        arrival_location_code = utils.random_string()
        arrival_location_name = utils.random_string()
        departure_time = utils.random_datetime()
        arrival_time = utils.random_datetime()
        loading_carrier_movement = CarrierMovement(
            Location(departure_location_code, departure_location_name),
            Location(arrival_location_code, arrival_location_name),
            departure_time,
            utils.random_string(),
            arrival_time,
        )
        unloading_carrier_movement = CarrierMovement(
            Location(departure_location_code, departure_location_name),
            Location(arrival_location_code, arrival_location_name),
            departure_time,
        )
        loading_handling_event = handling_event_factory.create(
            HandlingEventFactoryConfig(
                loading_carrier_movement,
                departure_time,
                loading_event_type,
            ),
        )
        loading_handling_event.carrier_movement = loading_carrier_movement
        unloading_handling_event = handling_event_factory.create(
            HandlingEventFactoryConfig(
                unloading_carrier_movement,
                arrival_time,
                unloading_event_type,
            )
        )
        unloading_handling_event.carrier_movement = unloading_carrier_movement
        cargo.delivery_history.add(loading_handling_event)
        cargo.delivery_history.add(unloading_handling_event)
        cargo_repository.save(cargo)

        # 2. Execute
        response = client.get(f"/tracking/history?tracking_id={tracking_id}")

        # 3. Assert
        response_body = response.json()
        assert response.status_code == 200
        assert response_body["history"][0]["event_type"] == loading_event_type
        assert response_body["history"][0][
            "completion_time"
        ] == departure_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert (
            response_body["history"][0]["carrier_movement"][
                "departure_location"
            ]["code"]
            == departure_location_code
        )
        assert (
            response_body["history"][0]["carrier_movement"][
                "departure_location"
            ]["name"]
            == departure_location_name
        )
        assert (
            response_body["history"][0]["carrier_movement"][
                "arrival_location"
            ]["code"]
            == arrival_location_code
        )
        assert (
            response_body["history"][0]["carrier_movement"][
                "arrival_location"
            ]["name"]
            == arrival_location_name
        )
        assert response_body["history"][0]["carrier_movement"][
            "departure_time"
        ] == departure_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert response_body["history"][0]["carrier_movement"][
            "arrival_time"
        ] == arrival_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert (
            response_body["history"][1]["event_type"] == unloading_event_type
        )
        assert response_body["history"][1][
            "completion_time"
        ] == arrival_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert (
            response_body["history"][1]["carrier_movement"][
                "departure_location"
            ]["code"]
            == departure_location_code
        )
        assert (
            response_body["history"][1]["carrier_movement"][
                "departure_location"
            ]["name"]
            == departure_location_name
        )
        assert (
            response_body["history"][1]["carrier_movement"][
                "arrival_location"
            ]["code"]
            == arrival_location_code
        )
        assert (
            response_body["history"][1]["carrier_movement"][
                "arrival_location"
            ]["name"]
            == arrival_location_name
        )
        assert response_body["history"][1]["carrier_movement"][
            "departure_time"
        ] == departure_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert (
            response_body["history"][1]["carrier_movement"]["arrival_time"]
            is None
        )
