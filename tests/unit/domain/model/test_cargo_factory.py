from datetime import datetime

from cargo_shipping.domain.model.cargo.cargo_factory import CargoFactory
from cargo_shipping.domain.model.cargo.delivery_specification import (
    DeliverySpecification,
)
from cargo_shipping.domain.model.handling.handling_event_factory import (
    HandlingEventFactory,
)
from cargo_shipping.domain.model.location.location import Location
from tests import utils


class TestCargoFactory:
    def test_create_success(self):
        """
        1. Prepare
        """
        factory = CargoFactory(HandlingEventFactory())

        id = utils.random_string()
        destination_code = utils.random_string()
        destination_name = utils.random_string()
        destination = Location(destination_code, destination_name)
        deadline = utils.random_datetime()

        """
        2. Execute
        """
        cargo = factory.create(id, destination, deadline)

        """
        3. Assert
        """
        assert cargo.id == id
        assert cargo.delivery_specification == DeliverySpecification(
            destination, deadline
        )
        assert cargo.delivery_history.handling_events == []

    def test_create_from_dict_success(self):
        """
        1. Prepare
        """
        factory = CargoFactory(HandlingEventFactory())

        cargo_id = utils.random_string()
        destination_name = utils.random_string()
        destination_code = utils.random_string()
        deadline = utils.random_datetime()
        delivery_history_id = utils.random_string()
        loading_event_type = "LOADING"
        loading_event_completion_time = utils.random_datetime()
        loading_carrier_movement_id = utils.random_string()
        unloading_event_type = "UNLOADING"
        unloading_event_completion_time = utils.random_datetime()
        unloading_carrier_movement_id = utils.random_string()
        departure_location_code = utils.random_string()
        departure_location_name = utils.random_string()
        arrival_location_name = utils.random_string()
        arrival_location_code = utils.random_string()
        departure_time = utils.random_datetime()
        arrival_time = utils.random_datetime()
        cargo_dict = {
            "id": cargo_id,
            "delivery_specification": {
                "destination": {
                    "code": destination_code,
                    "name": destination_name,
                },
                "deadline": deadline,
            },
            "delivery_history": {
                "id": delivery_history_id,
                "handling_events": [
                    {
                        "type": loading_event_type,
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
                    },
                    {
                        "type": unloading_event_type,
                        "completion_time": unloading_event_completion_time,
                        "carrier_movement": {
                            "id": unloading_carrier_movement_id,
                            "departure_location": {
                                "name": departure_location_name,
                                "code": departure_location_code,
                            },
                            "arrival_location": {
                                "name": arrival_location_name,
                                "code": arrival_location_code,
                            },
                            "departure_time": departure_time,
                            "arrival_time": "",
                        },
                    },
                ],
            },
        }

        """
        2. Execute
        """
        cargo = factory.create_from_dict(cargo_dict)

        """
        3. Assert
        """
        assert cargo.id == cargo_id
        assert (
            cargo.delivery_specification.destination.code == destination_code
        )
        assert (
            cargo.delivery_specification.destination.name == destination_name
        )
        assert cargo.delivery_specification.deadline == deadline
        assert cargo.delivery_history.id == delivery_history_id
        assert (
            cargo.delivery_history.handling_events[0].type
            == loading_event_type
        )
        assert (
            cargo.delivery_history.handling_events[0].completion_time
            == loading_event_completion_time
        )
        assert (
            cargo.delivery_history.handling_events[0].carrier_movement.id
            == loading_carrier_movement_id
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
            == departure_time
        )
        assert (
            cargo.delivery_history.handling_events[
                0
            ].carrier_movement.arrival_time
            == arrival_time
        )
        assert (
            cargo.delivery_history.handling_events[1].type
            == unloading_event_type
        )
        assert (
            cargo.delivery_history.handling_events[1].completion_time
            == unloading_event_completion_time
        )
        assert (
            cargo.delivery_history.handling_events[1].carrier_movement.id
            == unloading_carrier_movement_id
        )
        assert (
            cargo.delivery_history.handling_events[
                1
            ].carrier_movement.departure_location.code
            == departure_location_code
        )
        assert (
            cargo.delivery_history.handling_events[
                1
            ].carrier_movement.departure_location.name
            == departure_location_name
        )
        assert (
            cargo.delivery_history.handling_events[
                1
            ].carrier_movement.arrival_location.code
            == arrival_location_code
        )
        assert (
            cargo.delivery_history.handling_events[
                1
            ].carrier_movement.arrival_location.name
            == arrival_location_name
        )
        assert (
            cargo.delivery_history.handling_events[
                1
            ].carrier_movement.departure_time
            == departure_time
        )
        assert (
            cargo.delivery_history.handling_events[
                1
            ].carrier_movement.arrival_time
            == ""
        )
