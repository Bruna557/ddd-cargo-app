"""End-to-end tests."""

from fastapi.testclient import TestClient

from cargo_shipping.api.dependencies import (
    get_cargo_factory,
    get_cargo_repository,
)
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


def override_get_cargo_factory():
    """Override get_cargo_factory."""

    return cargo_factory


def override_get_cargo_repository():
    """Override get_cargo_repository."""

    return cargo_repository


app.dependency_overrides[get_cargo_factory] = override_get_cargo_factory
app.dependency_overrides[get_cargo_repository] = override_get_cargo_repository
client = TestClient(app)


class TestBookingApi:
    """Test Booking API."""

    def test_create_booking(self):
        """Test create_booking method."""

        # 1. Prepare
        tracking_id = utils.random_string()
        destination_code = utils.random_string()
        destination_name = utils.random_string()
        deadline = utils.random_datetime()

        # 2. Execute
        response = client.post(
            "/booking",
            headers={"Content-Type": "application/json"},
            json={
                "tracking_id": tracking_id,
                "destination": {
                    "code": destination_code,
                    "name": destination_name,
                },
                "deadline": deadline.strftime("%Y-%m-%d %H:%M:%S"),
            },
        )

        # 3. Assert
        cargo = cargo_repository.find_by_tracking_id(tracking_id)
        assert response.status_code == 201
        assert (
            cargo.delivery_specification.destination.code == destination_code
        )
        assert (
            cargo.delivery_specification.destination.name == destination_name
        )
        assert cargo.delivery_specification.deadline == deadline

    def test_get_booking(self):
        """Test get_booking method."""

        # 1. Prepare
        tracking_id = utils.random_string()
        destination_code = utils.random_string()
        destination_name = utils.random_string()
        destination = Location(destination_code, destination_name)
        deadline = utils.random_datetime()
        cargo = cargo_factory.create(
            CargoFactoryConfig(tracking_id, destination, deadline)
        )

        carrier_movement_id = utils.random_string()
        handling_event_id = utils.random_string()
        departure_location_code = utils.random_string()
        departure_location_name = utils.random_string()
        arrival_location_code = utils.random_string()
        arrival_location_name = utils.random_string()
        departure_time = utils.random_datetime()
        arrival_time = utils.random_datetime()
        event_type = HandlingEventTypes.LOADING
        carrier_movement = CarrierMovement(
            Location(departure_location_code, departure_location_name),
            Location(arrival_location_code, arrival_location_name),
            departure_time,
            carrier_movement_id,
            arrival_time,
        )
        handling_event = handling_event_factory.create(
            HandlingEventFactoryConfig(
                carrier_movement, departure_time, event_type, handling_event_id
            )
        )
        cargo.delivery_history.add(handling_event)
        cargo_repository.save(cargo)

        # 2. Execute
        response = client.get(f"/booking?tracking_id={tracking_id}")

        # 3. Assert
        response_body = response.json()
        assert response.status_code == 200
        assert response_body["entity_id"] == tracking_id
        assert (
            response_body["delivery_specification"]["destination"]["code"]
            == destination_code
        )
        assert (
            response_body["delivery_specification"]["destination"]["name"]
            == destination_name
        )
        assert response_body["delivery_specification"][
            "deadline"
        ] == deadline.strftime("%Y-%m-%dT%H:%M:%S")
        assert (
            response_body["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["departure_location"]["code"]
            == departure_location_code
        )
        assert (
            response_body["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["departure_location"]["name"]
            == departure_location_name
        )
        assert (
            response_body["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["arrival_location"]["code"]
            == arrival_location_code
        )
        assert (
            response_body["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["arrival_location"]["name"]
            == arrival_location_name
        )
        assert response_body["delivery_history"]["handling_events"][0][
            "carrier_movement"
        ]["departure_time"] == departure_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert response_body["delivery_history"]["handling_events"][0][
            "carrier_movement"
        ]["arrival_time"] == arrival_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert response_body["delivery_history"]["handling_events"][0][
            "completion_time"
        ] == departure_time.strftime("%Y-%m-%dT%H:%M:%S")
        assert (
            response_body["delivery_history"]["handling_events"][0][
                "event_type"
            ]
            == event_type
        )
