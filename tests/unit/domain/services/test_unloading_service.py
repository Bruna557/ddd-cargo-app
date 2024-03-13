"""Unit test."""

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
from cargo_shipping.domain.services.unloading_service import (
    UnloadingService,
    UnloadingServiceConfig,
)
from tests import utils
from tests.unit.mocks import FakeCargoRepository, FakeCarrierMovementRepository


class TestUnLoadingService:
    """Unloading Service Tests."""

    def test_execute_success(self):
        """Test execute method when should be successful."""

        # 1. Prepare
        handling_event_factory = HandlingEventFactory()
        cargo_repository = FakeCargoRepository()
        carrier_movement_repository = FakeCarrierMovementRepository()
        unloading_service = UnloadingService(
            handling_event_factory,
            cargo_repository,
            carrier_movement_repository,
        )

        # 1.1 create cargo booking
        cargo_factory = CargoFactory(handling_event_factory)
        tracking_id = utils.random_string()
        destination = Location(utils.random_string(), utils.random_string())
        deadline = utils.random_datetime()
        cargo = cargo_factory.create(
            CargoFactoryConfig(tracking_id, destination, deadline)
        )

        # 1.2 create loading carrier movement
        departure_location = Location(
            utils.random_string(), utils.random_string()
        )
        arrival_location = Location(
            utils.random_string(), utils.random_string()
        )
        departure_time = utils.random_datetime()
        arrival_time = utils.random_datetime()
        carrier_movement = CarrierMovement(
            departure_location, arrival_location, departure_time
        )
        carrier_movement_repository.save(carrier_movement)

        # 1.3 add loading handling event
        handling_event = handling_event_factory.create(
            HandlingEventFactoryConfig(
                carrier_movement, departure_time, HandlingEventTypes.LOADING
            )
        )
        cargo.delivery_history.add(handling_event)
        cargo_repository.save(cargo)

        # 2. Execute
        unloading_service_config = UnloadingServiceConfig(
            tracking_id, arrival_time
        )
        unloading_service.execute(unloading_service_config)

        # 3. Assert
        byproduct_handling_event = cargo.delivery_history.handling_events[1]
        assert (
            byproduct_handling_event.event_type == HandlingEventTypes.UNLOADING
        )
        assert byproduct_handling_event.completion_time == arrival_time
        assert (
            byproduct_handling_event.carrier_movement.departure_location
            == departure_location
        )
        assert (
            byproduct_handling_event.carrier_movement.arrival_location
            == arrival_location
        )
        assert (
            byproduct_handling_event.carrier_movement.departure_time
            == departure_time
        )
        assert (
            byproduct_handling_event.carrier_movement.arrival_time
            == arrival_time
        )
        assert carrier_movement.arrival_time == arrival_time
