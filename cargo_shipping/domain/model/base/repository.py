"""Define the Repository base class."""

import abc

from cargo_shipping.domain.model.base.entity import Entity


class Repository(abc.ABC):
    """In DDD a Repository is an object that abstracts away storage details."""

    @abc.abstractmethod
    def save(self, entity: Entity) -> None:
        """Save an Entity in the database."""

        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_key(self, key_name: str, key: str) -> dict:
        """Get an Entity from the database filtered by a key."""

        raise NotImplementedError()
