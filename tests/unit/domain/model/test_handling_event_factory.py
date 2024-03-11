"""Test file."""

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


class TestHandlingEventFactory:
    """Handling Event Factory Tests."""

    def test_create(self):
        """Test create method."""

        # 1. Prepare
        factory = HandlingEventFactory()
        departure_location = Location(
            utils.random_string(), utils.random_string()
        )
        arrival_location = Location(
            utils.random_string(), utils.random_string()
        )
        departure_time = utils.random_datetime()
        loaded_onto = CarrierMovement(
            departure_location, arrival_location, departure_time
        )
        time_stamp = utils.random_datetime()
        handling_event_type = HandlingEventTypes.LOADING

        # 2. Execute
        handling_event = factory.create(
            HandlingEventFactoryConfig(
                loaded_onto, time_stamp, handling_event_type
            )
        )

        # 3. Assert
        assert handling_event.carrier_movement == loaded_onto
        assert handling_event.completion_time == time_stamp
        assert handling_event.event_type == handling_event_type

    def test_create_from_dict(self):
        """Test create_from_dict method."""

        # 1. Prepare
        factory = HandlingEventFactory()

        entity_id = utils.random_string()
        loading_event_type = "LOADING"
        loading_event_completion_time = utils.random_datetime()
        loading_carrier_movement_id = utils.random_string()
        departure_location_code = utils.random_string()
        departure_location_name = utils.random_string()
        arrival_location_name = utils.random_string()
        arrival_location_code = utils.random_string()
        departure_time = utils.random_datetime()
        arrival_time = utils.random_datetime()
        handling_event_dict = {
            "entity_id": entity_id,
            "event_type": loading_event_type,
            "completion_time": loading_event_completion_time,
            "carrier_movement": {
                "id": loading_carrier_movement_id,
                "departure_location": {
                    "code": departure_location_code,
                    "name": departure_location_name,
                },
                "arrival_location": {
                    "code": arrival_location_code,
                    "name": arrival_location_name,
                },
                "departure_time": departure_time,
                "arrival_time": arrival_time,
            },
        }

        # 2. Execute
        handling_event = factory.create_from_dict(handling_event_dict)

        # 3. Assert
        assert handling_event.entity_id == entity_id
        assert handling_event.event_type == loading_event_type
        assert handling_event.completion_time == loading_event_completion_time
        assert (
            handling_event.carrier_movement.entity_id
            == loading_carrier_movement_id
        )
        assert (
            handling_event.carrier_movement.departure_location.code
            == departure_location_code
        )
        assert (
            handling_event.carrier_movement.departure_location.name
            == departure_location_name
        )
        assert (
            handling_event.carrier_movement.arrival_location.code
            == arrival_location_code
        )
        assert (
            handling_event.carrier_movement.arrival_location.name
            == arrival_location_name
        )
        assert handling_event.carrier_movement.departure_time == departure_time
        assert handling_event.carrier_movement.arrival_time == arrival_time
