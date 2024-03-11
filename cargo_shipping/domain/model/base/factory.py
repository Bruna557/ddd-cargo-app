"""Define the Factory base class."""

import abc

from cargo_shipping.domain.model.base.entity import Entity


class FactoryConfig(abc.ABC):
    """Configure arguments for the Factory.create() method."""


class Factory(abc.ABC):
    """In DDD, Factories are responsible for creating complex objects."""

    @abc.abstractmethod
    def create(self, config: FactoryConfig) -> Entity:
        """This method creates a new Entity."""

        raise NotImplementedError

    @abc.abstractmethod
    def create_from_dict(self, d: dict) -> Entity:
        """
        This method rebuilds the Entity from its dictionary implementation.
        """
        raise NotImplementedError
