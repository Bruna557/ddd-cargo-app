from cargo_shipping.domain.model.cargo.delivery_history import DeliveryHistory
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingActivity,
    HandlingEvent,
)
from cargo_shipping.domain.model.location.location import Location
from tests import utils


class TestDeliveryHistory:
    def test_add(self):
        """
        1. Prepare
        """
        delivery_history = DeliveryHistory()
        loading_carrier_movement = CarrierMovement(
            Location(utils.random_string(), utils.random_string()),
            Location(utils.random_string(), utils.random_string()),
            utils.random_datetime(),
            utils.random_string(),
            utils.random_datetime(),
        )
        unloading_carrier_movement = CarrierMovement(
            Location(utils.random_string(), utils.random_string()),
            Location(utils.random_string(), utils.random_string()),
            utils.random_datetime(),
            utils.random_string(),
        )
        loading_handling_event = HandlingEvent(
            HandlingActivity.LOADING, utils.random_datetime()
        )
        loading_handling_event.carrier_movement = loading_carrier_movement
        unloading_handling_event = HandlingEvent(
            HandlingActivity.UNLOADING, utils.random_datetime()
        )
        unloading_handling_event.carrier_movement = unloading_carrier_movement

        """
        2. Execute
        """
        delivery_history.add(loading_handling_event)
        delivery_history.add(unloading_handling_event)

        """
        3. Assert
        """
        assert delivery_history.handling_events[0] == loading_handling_event
        assert delivery_history.handling_events[1] == unloading_handling_event

    def test_latest_carrier_movement(self):
        """
        1. Prepare
        """
        delivery_history = DeliveryHistory()
        loading_carrier_movement = CarrierMovement(
            Location(utils.random_string(), utils.random_string()),
            Location(utils.random_string(), utils.random_string()),
            utils.random_datetime(),
            utils.random_string(),
            utils.random_datetime(),
        )
        unloading_carrier_movement = CarrierMovement(
            Location(utils.random_string(), utils.random_string()),
            Location(utils.random_string(), utils.random_string()),
            utils.random_datetime(),
            utils.random_string(),
        )
        loading_handling_event = HandlingEvent(
            HandlingActivity.LOADING, utils.random_datetime()
        )
        loading_handling_event.carrier_movement = loading_carrier_movement
        unloading_handling_event = HandlingEvent(
            HandlingActivity.UNLOADING, utils.random_datetime()
        )
        unloading_handling_event.carrier_movement = unloading_carrier_movement
        delivery_history.add(loading_handling_event)
        delivery_history.add(unloading_handling_event)

        """
        2. Execute
        """
        latest_carrier_movement = delivery_history.latest_carrier_movement

        """
        3. Assert
        """
        assert latest_carrier_movement == unloading_carrier_movement

    def test_current_location(self):
        """
        Case A: Arrival time is None
        """
        """
        A1. Prepare
        """
        delivery_history = DeliveryHistory()
        departure_location = Location(
            utils.random_string(), utils.random_string()
        )
        arrival_location = Location(
            utils.random_string(), utils.random_string()
        )
        loading_carrier_movement = CarrierMovement(
            departure_location,
            arrival_location,
            utils.random_datetime(),
            utils.random_string(),
            utils.random_datetime(),
        )
        unloading_carrier_movement = CarrierMovement(
            departure_location,
            arrival_location,
            utils.random_datetime(),
        )
        loading_handling_event = HandlingEvent(
            HandlingActivity.LOADING, utils.random_datetime()
        )
        loading_handling_event.carrier_movement = loading_carrier_movement
        unloading_handling_event = HandlingEvent(
            HandlingActivity.UNLOADING, utils.random_datetime()
        )
        unloading_handling_event.carrier_movement = unloading_carrier_movement
        delivery_history.add(loading_handling_event)
        delivery_history.add(unloading_handling_event)

        """
        A2. Execute
        """
        current_location = delivery_history.current_location

        """
        A3. Assert
        """
        assert current_location == departure_location

        """
        Case B Arrival time is not None
        """
        """
        B1. Prepare
        """
        unloading_carrier_movement.set_arrival_time(utils.random_datetime())

        """
        B2. Execute
        """
        current_location = delivery_history.current_location

        """
        B3. Assert
        """
        assert current_location == arrival_location

    def test_to_dict(self):
        """
        1. Prepare
        """
        id = utils.random_string()
        delivery_history = DeliveryHistory(id)
        departure_location_code = utils.random_string()
        departure_location_name = utils.random_string()
        departure_location = Location(
            departure_location_code, departure_location_name
        )
        arrival_location_code = utils.random_string()
        arrival_location_name = utils.random_string()
        arrival_location = Location(
            arrival_location_code, arrival_location_name
        )
        departure_time = utils.random_datetime()
        arrival_time = utils.random_datetime()
        loading_carrier_movement_id = utils.random_string()
        loading_completion_time = utils.random_datetime()
        unloading_carrier_movement_id = utils.random_string()
        unloading_completion_time = utils.random_datetime()
        loading_carrier_movement = CarrierMovement(
            departure_location,
            arrival_location,
            departure_time,
            loading_carrier_movement_id,
            arrival_time,
        )
        unloading_carrier_movement = CarrierMovement(
            departure_location,
            arrival_location,
            departure_time,
            unloading_carrier_movement_id,
        )

        loading_handling_event = HandlingEvent(
            HandlingActivity.LOADING, loading_completion_time
        )
        loading_handling_event.carrier_movement = loading_carrier_movement
        unloading_handling_event = HandlingEvent(
            HandlingActivity.UNLOADING, unloading_completion_time
        )
        unloading_handling_event.carrier_movement = unloading_carrier_movement
        delivery_history.add(loading_handling_event)
        delivery_history.add(unloading_handling_event)

        """
        2. Execute
        """
        delivery_history_dict = delivery_history.to_dict()

        """
        3. Assert
        """
        assert delivery_history_dict["id"] == id
        assert (
            delivery_history_dict["handling_events"][0]["type"]
            == HandlingActivity.LOADING
        )
        assert (
            delivery_history_dict["handling_events"][0]["completion_time"]
            == loading_completion_time
        )
        assert (
            delivery_history_dict["handling_events"][0]["carrier_movement"][
                "id"
            ]
            == loading_carrier_movement_id
        )
        assert (
            delivery_history_dict["handling_events"][0]["carrier_movement"][
                "departure_location"
            ]["code"]
            == departure_location_code
        )
        assert (
            delivery_history_dict["handling_events"][0]["carrier_movement"][
                "departure_location"
            ]["name"]
            == departure_location_name
        )
        assert (
            delivery_history_dict["handling_events"][0]["carrier_movement"][
                "arrival_location"
            ]["code"]
            == arrival_location_code
        )
        assert (
            delivery_history_dict["handling_events"][0]["carrier_movement"][
                "arrival_location"
            ]["name"]
            == arrival_location_name
        )
        assert (
            delivery_history_dict["handling_events"][0]["carrier_movement"][
                "departure_time"
            ]
            == departure_time
        )
        assert (
            delivery_history_dict["handling_events"][0]["carrier_movement"][
                "arrival_time"
            ]
            == arrival_time
        )
        assert (
            delivery_history_dict["handling_events"][1]["type"]
            == HandlingActivity.UNLOADING
        )
        assert (
            delivery_history_dict["handling_events"][1]["completion_time"]
            == unloading_completion_time
        )
        assert (
            delivery_history_dict["handling_events"][1]["carrier_movement"][
                "id"
            ]
            == unloading_carrier_movement_id
        )
        assert (
            delivery_history_dict["handling_events"][1]["carrier_movement"][
                "departure_location"
            ]["code"]
            == departure_location_code
        )
        assert (
            delivery_history_dict["handling_events"][1]["carrier_movement"][
                "departure_location"
            ]["name"]
            == departure_location_name
        )
        assert (
            delivery_history_dict["handling_events"][1]["carrier_movement"][
                "arrival_location"
            ]["code"]
            == arrival_location_code
        )
        assert (
            delivery_history_dict["handling_events"][1]["carrier_movement"][
                "arrival_location"
            ]["name"]
            == arrival_location_name
        )
        assert (
            delivery_history_dict["handling_events"][1]["carrier_movement"][
                "departure_time"
            ]
            == departure_time
        )
        assert (
            delivery_history_dict["handling_events"][1]["carrier_movement"][
                "arrival_time"
            ]
            is None
        )
