from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingActivity,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from tests import utils


class TestHandlingEventFactory:
    def test_create(self):
        """
        1. Prepare
        """
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
        activity = HandlingActivity.LOADING

        """
        2. Execute
        """
        handling_event = factory.create(loaded_onto, time_stamp, activity)

        """
        3. Assert
        """
        assert handling_event.carrier_movement == loaded_onto
        assert handling_event.completion_time == time_stamp
        assert handling_event.type == activity
