"""Define the Aggregate Root base class."""

from cargo_shipping.domain.model.base.entity import Entity


class AggregateRoot(Entity):
    """
    In DDD, an Aggregate is a cluster of related objects that form a
    consistency boundary and are treated as a single unit. An aggregate root is
    the entity that controls the access and behavior of the other objects in
    the aggregate.
    """

    def __init__(self, aggregate_root_id) -> None:
        Entity.__init__(self, aggregate_root_id)
