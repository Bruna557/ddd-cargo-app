"""Test file."""

from cargo_shipping.domain.model.carrier.carrier_movement import (
    CarrierMovement,
)
from cargo_shipping.domain.model.location.location import Location
from tests import utils


class TestCarrierMovement:
    """Carrier Movement Tests."""

    def test_set_arrival_time(self):
        """Test set_arrival_time method."""

        # 1. Prepare
        departure_location = Location(
            utils.random_string(), utils.random_string()
        )
        arrival_location = Location(
            utils.random_string(), utils.random_string()
        )
        departure_time = utils.random_datetime()
        carrier_movement = CarrierMovement(
            departure_location, arrival_location, departure_time
        )

        # 2. Execute
        arrival_time = utils.random_datetime()
        carrier_movement.set_arrival_time(arrival_time)

        # 3. Assert
        assert carrier_movement.arrival_time == arrival_time

    def test_to_dict(self):
        """Test to_dict method."""

        # 1. Prepare
        entity_id = utils.random_string()
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
        carrier_movement = CarrierMovement(
            departure_location,
            arrival_location,
            departure_time,
            entity_id,
            arrival_time,
        )

        # 2. Execute
        carrier_movement_dict = carrier_movement.to_dict()

        # 3. Assert
        assert carrier_movement_dict["entity_id"] == entity_id
        assert (
            carrier_movement_dict["departure_location"]["code"]
            == departure_location_code
        )
        assert (
            carrier_movement_dict["departure_location"]["name"]
            == departure_location_name
        )
        assert (
            carrier_movement_dict["arrival_location"]["code"]
            == arrival_location_code
        )
        assert (
            carrier_movement_dict["arrival_location"]["name"]
            == arrival_location_name
        )
        assert carrier_movement_dict["departure_time"] == departure_time
        assert carrier_movement_dict["arrival_time"] == arrival_time
