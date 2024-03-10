from datetime import datetime

from cargo_shipping.domain.model.cargo.cargo import Cargo
from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.cargo.delivery_history import DeliveryHistory
from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.handling.handling_event import (
    HandlingActivity,
    HandlingEvent,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from tests import utils


class TestCargo:
    def test_to_dict(self):
        """
        1. Prepare
        """
        cargo_id = utils.random_string()
        cargo = Cargo(cargo_id)
        factory = CargoFactory(HandlingEventFactory())

        destination_code = utils.random_string()
        destination_name = utils.random_string()
        destination = Location(destination_code, destination_name)
        deadline = utils.random_datetime()
        cargo = factory.create(cargo_id, destination, deadline)

        delivery_history_id = "HISTORY_ID"
        delivery_history = DeliveryHistory(delivery_history_id)

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

        cargo.delivery_history = delivery_history

        """
        2. Execute
        """
        cargo_dict = cargo.to_dict()

        """
        3. Assert
        """
        assert cargo_dict["id"] == cargo_id
        assert (
            cargo_dict["delivery_specification"]["destination"]["code"]
            == destination_code
        )
        assert (
            cargo_dict["delivery_specification"]["destination"]["name"]
            == destination_name
        )
        assert cargo_dict["delivery_specification"]["deadline"] == deadline
        assert cargo_dict["delivery_history"]["id"] == delivery_history_id
        assert (
            cargo_dict["delivery_history"]["handling_events"][0]["type"]
            == HandlingActivity.LOADING
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][0][
                "completion_time"
            ]
            == loading_completion_time
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["id"]
            == loading_carrier_movement_id
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["departure_location"]["code"]
            == departure_location_code
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["departure_location"]["name"]
            == departure_location_name
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["arrival_location"]["code"]
            == arrival_location_code
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["arrival_location"]["name"]
            == arrival_location_name
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["departure_time"]
            == departure_time
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][0][
                "carrier_movement"
            ]["arrival_time"]
            == arrival_time
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1]["type"]
            == HandlingActivity.UNLOADING
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1][
                "completion_time"
            ]
            == unloading_completion_time
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1][
                "carrier_movement"
            ]["id"]
            == unloading_carrier_movement_id
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1][
                "carrier_movement"
            ]["departure_location"]["code"]
            == departure_location_code
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1][
                "carrier_movement"
            ]["departure_location"]["name"]
            == departure_location_name
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1][
                "carrier_movement"
            ]["arrival_location"]["code"]
            == arrival_location_code
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1][
                "carrier_movement"
            ]["arrival_location"]["name"]
            == arrival_location_name
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1][
                "carrier_movement"
            ]["departure_time"]
            == departure_time
        )
        assert (
            cargo_dict["delivery_history"]["handling_events"][1][
                "carrier_movement"
            ]["arrival_time"]
            is None
        )
