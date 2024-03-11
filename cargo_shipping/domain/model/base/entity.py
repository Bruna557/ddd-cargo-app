"""Define the Entity base class."""

import abc
from dataclasses import dataclass


@dataclass
class Entity(abc.ABC):
    """In DDD, an Entity is an object that has an identity."""

    _entity_id: str

    def __eq__(self, other: object) -> bool:
        return self.entity_id == other.entity_id

    def __ne__(self, other: object) -> bool:
        return not self == other

    @abc.abstractmethod
    def to_dict(self) -> dict:
        """Get a dictionary representation of the Entity."""

        raise NotImplementedError

    @property
    def entity_id(self):
        """_entity_id getter."""

        return self._entity_id
