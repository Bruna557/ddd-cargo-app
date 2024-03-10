from cargo_shipping.domain.model.location.location import Location
from tests import utils


class TestLocation:
    def test_to_dict(self):
        """
        1. Prepare
        """
        code = utils.random_string()
        name = utils.random_string()
        location = Location(code, name)

        """
        2. Execute
        """
        location_dict = location.to_dict()

        """
        3. Assert
        """
        assert location_dict["code"] == code
        assert location_dict["name"] == name
