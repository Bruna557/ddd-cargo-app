from dataclasses import dataclass


@dataclass
class Entity(object):
    _entity_id: str

    def __eq__(self, other: object) -> bool:
        return self.id == other.id

    def __ne__(self, other: object) -> bool:
        return not self == other

    @property
    def id(self):
        return self._entity_id
