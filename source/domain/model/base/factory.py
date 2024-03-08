import abc

from source.domain.model.base.entity import Entity


class Factory(abc.ABC):
    @abc.abstractmethod
    def create(self, *args) -> Entity:
        raise NotImplementedError
