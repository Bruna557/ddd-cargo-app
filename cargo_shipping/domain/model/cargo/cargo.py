"""Cargo Aggregate Root implementation."""

from enum import Enum

from cargo_shipping.domain.model.base.aggregate_root import AggregateRoot
from cargo_shipping.domain.model.cargo.delivery_history import DeliveryHistory


class Role(Enum):
    """Possible user roles."""

    SHIPPER = "SHIPPER"
    RECEIVER = "RECEIVER"
    PAYER = "PAYER"


class Cargo(AggregateRoot):
    """
    Cargo is an Agreggate Root that represents an object to be shipped.
    Cargos have a entity_id (entity_id), a Delivery History and a Delivery
    Specification.
    """

    def __init__(self, entity_id: str) -> None:
        AggregateRoot.__init__(self, entity_id)
        self.delivery_history = DeliveryHistory()
        self.delivery_specification = None

    def to_dict(self) -> dict:
        dict_ = {
            "entity_id": self.entity_id,
            "delivery_specification": self.delivery_specification.to_dict(),
            "delivery_history": self.delivery_history.to_dict(),
        }
        return dict_
