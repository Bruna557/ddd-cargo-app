"""Define the Domain Service base class."""

import abc


class DomainServiceConfig(abc.ABC):
    """Configure arguments for the DomainService.execute() method."""


class DomainService(abc.ABC):
    """
    In DDD, Domain Services contains domain logic that doesn't belong to an
    Entity or Value Object. They are used to perform domain operations and
    business rules.
    """

    @abc.abstractmethod
    def execute(self, config: DomainServiceConfig) -> None:
        """This method executes the Domain Service Logic."""

        raise NotImplementedError
