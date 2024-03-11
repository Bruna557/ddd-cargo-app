"""Test file."""

from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingEvent,
    HandlingEventTypes,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
    HandlingEventFactoryConfig,
)
from cargo_shipping.domain.model.location.location import Location
from tests import utils


class TestHandlingEvent:
    """Handling Event Tests."""

    def test_set_carrier_movement(self):
        """Test set_carrier_movement method."""

        # 1. Prepare
        handling_event = HandlingEvent(
            utils.random_string(),
            HandlingEventTypes.LOADING,
            utils.random_datetime(),
        )
        carrier_movement = CarrierMovement(
            Location(utils.random_string(), utils.random_string()),
            Location(utils.random_string(), utils.random_string()),
            utils.random_datetime(),
        )

        # 2. Execute
        handling_event.set_carrier_movement(carrier_movement)

        # 3. Assert
        assert handling_event.carrier_movement == carrier_movement

    def test_to_dict(self):
        """Test to_dict method."""

        # 1. Prepare
        handling_event_factory = HandlingEventFactory()
        handling_event_id = utils.random_string()
        carrier_movement_id = utils.random_string()
        departure_location_code = utils.random_string()
        departure_location_name = utils.random_string()
        arrival_location_code = utils.random_string()
        arrival_location_name = utils.random_string()
        departure_time = utils.random_datetime()
        arrival_time = utils.random_datetime()
        loaded_onto = CarrierMovement(
            Location(departure_location_code, departure_location_name),
            Location(arrival_location_code, arrival_location_name),
            departure_time,
            carrier_movement_id,
            arrival_time,
        )
        handling_event_type = HandlingEventTypes.LOADING
        handling_event = handling_event_factory.create(
            HandlingEventFactoryConfig(
                loaded_onto,
                departure_time,
                handling_event_type,
                handling_event_id,
            )
        )

        # 2. Execute
        handling_event_dict = handling_event.to_dict()

        # 3. Assert
        assert handling_event_dict["entity_id"] == handling_event_id
        assert (
            handling_event_dict["carrier_movement"]["departure_location"][
                "code"
            ]
            == departure_location_code
        )
        assert (
            handling_event_dict["carrier_movement"]["departure_location"][
                "name"
            ]
            == departure_location_name
        )
        assert (
            handling_event_dict["carrier_movement"]["arrival_location"]["code"]
            == arrival_location_code
        )
        assert (
            handling_event_dict["carrier_movement"]["arrival_location"]["name"]
            == arrival_location_name
        )
        assert (
            handling_event_dict["carrier_movement"]["departure_time"]
            == departure_time
        )
        assert (
            handling_event_dict["carrier_movement"]["arrival_time"]
            == arrival_time
        )
        assert handling_event_dict["completion_time"] == departure_time
        assert handling_event_dict["event_type"] == handling_event_type
