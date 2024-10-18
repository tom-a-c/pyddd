import functools
from typing import Any, Callable, Optional, Type, TypeVar


class EntityException(Exception):
    pass


EntityDecInstType = TypeVar('EntityDecInstType', bound=Any)
# Classes decorated with `@entity` will be of this type.
EntityDecClsType = Type[EntityDecInstType]


class NoEntityIDException(EntityException):
    def __init__(self, cls: EntityDecClsType) -> None:
        super().__init__(f"Entity '{cls.__name__}' must have a unique ID")


class _Entity:

    def __init__(self, cls: EntityDecClsType, id_attr: Optional[str]) -> None:
        self.cls = cls
        self.id_attr = id_attr

    def __call__(self, *args: Any, **kwargs: Any) -> EntityDecInstType:
        return self.cls(*args, **kwargs)

    def _enforce_unique_id(self) -> None:
        orig_init = self.cls.__init__

        def new_init(inst, *args: Any, **kwargs: Any) -> None:
            orig_init(inst, *args, **kwargs)
            if getattr(inst, self.id_attr) is None:
                raise NoEntityIDException(self.cls)

        self.cls.__init__ = new_init


EntityDecFactoryType = Callable[[EntityDecClsType], _Entity]


def entity(unique_id_attr: Optional[str] = None) -> EntityDecFactoryType:
    """
    Entity decorator factory.
    :param unique_id_attr:
    :return: A domain model entity decorator
    """
    def decorator(cls: EntityDecClsType) -> _Entity:
        return functools.wraps(cls, updated=())(_Entity(cls, unique_id_attr))
    return decorator
