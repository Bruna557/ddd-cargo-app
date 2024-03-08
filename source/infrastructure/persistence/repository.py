import abc

from source.domain.model.base.entity import Entity


class Repository(Entity, abc.ABC):
    @abc.abstractmethod
    def save(self, entity: Entity):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, id: str) -> Entity:
        raise NotImplementedError()
