"""Test file."""

from cargo_shipping.domain.model.cargo.delivery_specification import (
    DeliverySpecification,
)
from cargo_shipping.domain.model.location.location import Location
from tests import utils


class TestDeliverySpecification:
    """Delivery Specification Tests."""

    def test_to_dict(self):
        """Test to_dict method."""

        # 1. Prepare
        destination_code = utils.random_string()
        destination_name = utils.random_string()
        destination = Location(destination_code, destination_name)
        deadline = utils.random_datetime()
        delivery_specification = DeliverySpecification(destination, deadline)

        # 2. Execute
        delivery_specification_dict = delivery_specification.to_dict()

        # 3. Assert
        assert (
            delivery_specification_dict["destination"]["code"]
            == destination_code
        )
        assert (
            delivery_specification_dict["destination"]["name"]
            == destination_name
        )
        assert delivery_specification_dict["deadline"] == deadline
