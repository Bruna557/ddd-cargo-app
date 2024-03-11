"""
Delivery Specification Value Object (included in the Cargo Aggregate)
implementation.
"""

from datetime import datetime

from cargo_shipping.domain.model.base.value_object import ValueObject
from cargo_shipping.domain.model.location.location import Location


class DeliverySpecification(ValueObject):
    """
    Delivery Specification is a Value Object that stores the destination and
    the deadline (the Cargo must be delivered before deadline) of a Cargo.
    """

    def __init__(self, destination: Location, deadline: datetime) -> None:
        self.destination = destination
        self.deadline = deadline

    def to_dict(self) -> dict:
        return {
            "destination": self.destination.to_dict(),
            "deadline": self.deadline,
        }
