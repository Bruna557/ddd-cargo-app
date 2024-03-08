from cargo_shipping.domain.model.base.entity import Entity


class Customer(Entity):
    def __init__(self, id: str, name: str) -> None:
        Entity.__init__(self, id)
        self.name = name
