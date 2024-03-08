from enum import Enum

from source.domain.model.base.aggregate import Aggregate
from source.domain.model.cargo.delivery_history import DeliveryHistory
from source.domain.model.customer.customer import Customer


class Role(Enum):
    SHIPPER = "SHIPPER"
    RECEIVER = "RECEIVER"
    PAYER = "PAYER"


class Cargo(Aggregate):
    def __init__(self, id: str) -> None:
        Aggregate.__init__(self, id)
        self.delivery_history = DeliveryHistory()
        self.customer_roles = dict[Customer, Role]
        self.delivery_specification = None
