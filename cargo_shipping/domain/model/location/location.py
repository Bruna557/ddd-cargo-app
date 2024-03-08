from cargo_shipping.domain.model.base.value_object import ValueObject


class Location(ValueObject):
    def __init__(self, name: str, code: str) -> None:
        self.name = name
        self.code = code
