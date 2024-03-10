import abc

from cargo_shipping.domain.model.base.entity import Entity


class Repository(abc.ABC):
    @abc.abstractmethod
    def save(self, entity: Entity) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_key(self, key_name: str, key: str) -> dict:
        raise NotImplementedError()
