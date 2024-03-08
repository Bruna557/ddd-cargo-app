from dataclasses import dataclass


@dataclass
class Entity(object):
    _id: str

    def __eq__(self, other: object) -> bool:
        return self.id == other.id

    def __ne__(self, other: object) -> bool:
        return not self == other

    @property
    def id(self) -> str:
        return self._id
