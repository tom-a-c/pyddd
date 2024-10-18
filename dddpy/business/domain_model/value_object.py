import functools

from dataclasses import dataclass
from typing import Any, Callable, Type, TypeVar, get_type_hints

__all__ = ['value_object', 'ImmutabilityException', 'get_value_objects']

# Instances of classes decorated with `@value_object` will be of this
# type.
VODecClsType = TypeVar('VODecClsType', bound=Any)


class ImmutabilityException(Exception):
    def __init__(self, vo: VODecClsType, attr: str) -> None:
        cls = type(vo).__name__
        msg = f"Cannot modify '{cls}.{attr}'; value objects are immutable"
        super().__init__(msg)


ConditionType = Callable[[VODecClsType], bool | tuple[bool, str]]
AttrType = TypeVar('AttrType')


class Conditioner:
    def __init__(self, name: str, type_hint: AttrType) -> None:
        self.name = name
        self.type_hint = type_hint
        self.preconditions: list[ConditionType] = []
        self.postconditions: list[ConditionType] = []

    def __set_name__(self, owner: Type[VODecClsType], name: str) -> None:
        self.name = name

    def __get__(self, instance: VODecClsType, owner: Type[VODecClsType]) -> AttrType:
        return instance.__dict__[self.name]

    def __set__(self, instance: VODecClsType, value: AttrType) -> None:
        instance.__dict__[self.name] = value

    def condition(self, func: ConditionType) -> ConditionType:
        self.precondition(func)
        self.postcondition(func)
        return func

    def precondition(self, func: ConditionType) -> ConditionType:
        self.preconditions.append(func)
        return func

    def postcondition(self, func: ConditionType) -> ConditionType:
        self.postconditions.append(func)
        return func

    def __repr__(self) -> str:
        fields = [self.name, self.type_hint]
        params = ', '.join(f"{field.__name__}={field}" for field in fields)
        return f"{self.__class__.__name__}(name={params})"


def condition_decorator(descriptor_method):
    """Decorator to allow stacking of decorators for multiple fields."""
    def decorator(func):
        def wrapper(descriptor):
            descriptor_method(descriptor, func)
            return func
        return wrapper
    return decorator


class ValueObjectMeta(type):
    def __new__(cls, name, bases, dct):
        # Convert type hints into ConditionDescriptors after class is defined
        cls_instance = super().__new__(cls, name, bases, dct)
        type_hints = get_type_hints(cls_instance)
        for attr_name, attr_type in type_hints.items():
            attr = getattr(cls_instance, attr_name, None)
            if not isinstance(attr, Conditioner):
                descriptor = Conditioner(attr_name, attr_type)
                setattr(cls_instance, attr_name, descriptor)
        return cls_instance

    def __getattr__(cls, attr):
        if attr in cls.__annotations__:
            # Dynamically create and return a ConditionDescriptor
            descriptor = Conditioner(attr, cls.__annotations__[attr])
            setattr(cls, attr, descriptor)
            return descriptor
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{attr}'")


class ValueObjectDecorator:
    """
    A decorator class that enforces immutability and overrides
    equality methods.

    This class is used as a decorator for other classes to enforce
    immutability and override equality methods. It uses Python's
    dataclasses to create a new class with the same attributes but
    with added immutability and equality methods.

    Examples::

        @ValueObject
        class MyClassA:
            x: int
            y: str

        my_instance = MyClass(5)
        my_instance.x = 10  # Raises AttributeError

    Warning:
        This class should only be used as a decorator for classes that
        do not have their own `__eq__` or `__hash__` methods.
    """
    _instance_cache: dict[tuple, VODecClsType] = {}
    _value_objects: list[Type[VODecClsType]] = []

    def __new__(cls, decorated_cls: Type[VODecClsType]) -> 'ValueObjectDecorator':
        decorated_cls_with_meta = type(
            decorated_cls.__name__,
            (decorated_cls,),
            {},
            metaclass=ValueObjectMeta
        )
        instance = super().__new__(cls)
        instance.decorated_cls = decorated_cls_with_meta
        return instance

    def __init__(self, wrapped_cls: Type[VODecClsType]) -> None:
        self.decorated_cls = dataclass(
            frozen=True,
            slots=True,
            order=True,
            kw_only=True
        )(wrapped_cls)
        self.enforce_immutability(self.decorated_cls)

        self._value_objects.append(self.decorated_cls)

    def __call__(self, *args: Any, **kwargs: Any) -> VODecClsType:
        return self.decorated_cls(*args, **kwargs)

    @classmethod
    def value_objects(cls) -> list[VODecClsType]:
        return cls._value_objects

    @staticmethod
    def enforce_immutability(cls: VODecClsType) -> None:
        def new_setattr(inst: VODecClsType, name: str, _: Any) -> None:
            raise ImmutabilityException(inst, name)
        cls.__setattr__ = new_setattr

    def apply_conditioners(self) -> None:
        for name, type_hint in get_type_hints(self.decorated_cls).items():
            attr = getattr(self.decorated_cls, name, None)
            if not isinstance(attr, Conditioner):
                setattr(self.decorated_cls, name, Conditioner(name, type_hint))

    def __repr__(self):
        return f"{self.__class__.__name__}(decorated_cls={self.decorated_cls})"


def get_value_objects() -> list[VODecClsType]:
    """
    Get all value object classes.
    :return:
    """
    return ValueObjectDecorator.value_objects()


VODecCallType = Callable[[Type[VODecClsType]], Type[VODecClsType]]
VODecReturnType = VODecCallType | Type[VODecClsType]


def value_object(cls: Type[VODecClsType] | None = None) -> VODecReturnType:
    """
    Value object decorator factory.
    """

    cls.x.__annotations__ = {'x': str}
    cls.x = 'c'

    def decorator(wrapped_cls: Type[VODecClsType]) -> Type[VODecClsType]:
        """
        Instantiates the value object decorator class and applies
        `functools.wraps` to preserve metadata.
        """
        decorator_instance = ValueObjectDecorator(wrapped_cls)
        new_cls = functools.wraps(wrapped_cls, updated=())(decorator_instance)
        return new_cls

    # Standardise `@value_object` and `@value_object()` usage.
    return decorator if cls is None else decorator(cls)
