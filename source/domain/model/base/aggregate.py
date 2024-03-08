from source.domain.model.base.entity import Entity


class Aggregate(Entity):
    def __init__(self, id) -> None:
        Entity.__init__(self, id)
