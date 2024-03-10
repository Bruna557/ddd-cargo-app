from enum import Enum

from cargo_shipping.domain.model.base.aggregate import Aggregate
from cargo_shipping.domain.model.cargo.delivery_history import DeliveryHistory


class Role(Enum):
    SHIPPER = "SHIPPER"
    RECEIVER = "RECEIVER"
    PAYER = "PAYER"


class Cargo(Aggregate):
    def __init__(self, id: str) -> None:
        Aggregate.__init__(self, id)
        self.delivery_history = DeliveryHistory()
        self.delivery_specification = None

    def to_dict(self) -> dict:
        dict_ = {
            "id": self.id,
            "delivery_specification": self.delivery_specification.to_dict(),
            "delivery_history": self.delivery_history.to_dict(),
        }
        return dict_
