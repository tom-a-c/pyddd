from typing import Any, TypeVar, Type, Union, Callable

from dddpy.business.domain_model.entity import _Entity
from dddpy.business.domain_model.value_object import ValueObjectDecorator


class AggregateCollection:

    def add(self):
        pass

    def get(self, name: str):
        pass


DomainObjType = TypeVar('DomainObjType', bound=Union[ValueObjectDecorator, _Entity])


class Aggregate:

    all_aggregates: AggregateCollection = {}

    def __init__(self, root: bool = False) -> None:
        self.root = root

    def __call__(self, cls: DomainObjType) -> DomainObjType:
        self._validate_entity_or_vo(cls)
        if self.root:
            self._validate_root_is_entity(cls)
        return cls

    @staticmethod
    def _validate_root_is_entity(cls: _Entity) -> None:
        if not isinstance(cls, _Entity):
            raise TypeError("Aggregate roots must be entities")

    @staticmethod
    def _validate_entity_or_vo(cls: DomainObjType) -> None:
        if not (isinstance(cls, ValueObjectDecorator) or isinstance(cls, _Entity)):
            raise TypeError(
                "Aggregates must only include entities and value objects")


def get_aggregates() -> AggregateCollection:
    return Aggregate.all_aggregates


aggregate = Aggregate
