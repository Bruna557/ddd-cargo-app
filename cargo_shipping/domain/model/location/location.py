from cargo_shipping.domain.model.base.value_object import ValueObject


class Location(ValueObject):
    def __init__(self, code: str, name: str) -> None:
        self.code = code
        self.name = name

    def to_dict(self) -> dict:
        return {"code": self.code, "name": self.name}
