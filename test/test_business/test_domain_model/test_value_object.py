from dataclasses import dataclass
from typing import Any

import pytest

from dddpy.business.domain_model.value_object import value_objec, value_object


def test_value_object_decorator_initialization_single_attribute():
    @value_object()
    class MyClass:
        def __init__(self, x):
            self.x = x

    # Test that the decorated class can be instantiated with a single
    # attribute
    my_instance = MyClass(5)
    assert my_instance.x == 5


def test_value_object_decorator_initialization_multiple_attributes():
    @value_object
    class MyClass:
        x: int
        y: int

        def __init__(self, x, y):
            self.x = x
            self.y = y

    # Test that the decorated class can be instantiated with multiple
    # attributes
    my_instance = MyClass(5, 10)
    assert my_instance.x == 5
    assert my_instance.y == 10


def test_value_object_decorator_immutability_single_attribute():
    @value_object
    class MyClass:
        def __init__(self, x):
            self.x = x

    # Test that the decorated class is immutable for a single attribute
    my_instance = MyClass(5)
    regex_match = "Cannot modify .*; value objects are immutable"
    with pytest.raises(AttributeError, match=regex_match):
        my_instance.x = 10


from typing import Callable, Any, Type


class PreconditionDescriptor:
    def __init__(self, attr_name: str, func: Callable[[Any], Any]) -> None:
        self.attr_name = attr_name
        self.func = func

    def __get__(self, instance: Any, owner: Type[Any]) -> Any:
        if instance is None:
            return self
        value = getattr(instance, self.attr_name)
        return self.func(value)


def precondition(attribute: object) -> Any:
    def decorator(func: Callable[[Any], Any]) -> PreconditionDescriptor:
        return PreconditionDescriptor(attribute.name, func)
    return decorator


def test_value_object_decorator_immutability_multiple_attributes():
    @aggregate(root=True)
    @value_object(auto_doc=True, strict=True)
    class MyClass:

        bob = field(int, conditions=(lambda x: (x > 0, 'positive'), ), auto_coerce).default(0)
        x = Conditioner(int)
        z: int

        @field
        @property
        def z(self) -> int:
            return self.bob * self.x

        @bob.coerce
        def to_vector(self, value: tuple[int, int]) -> int:
            return value[0] * value[1]

        @z.postcondition
        def positive(self, attr) -> bool | tuple[bool, str]:
            return attr > 0, "must be positive"

        @bob.precondition(safe=True)
        @x.precondition
        def positive(self, attr) -> bool | tuple[bool, str]:
            return attr > 0, "must be positive"

        @x.postcondition
        def is_positive(self) -> bool | tuple[bool, str]:
            return self.x > 0, "must be positive"

        @x.postcondition
        def is_even(self) -> bool | tuple[bool, str]:
            return (self.x % 2) == 0, "must be even"

    # Test that the decorated class is immutable for multiple attributes
    my_instance = MyClass(x=5, y=10)
    regex_match = "Cannot modify .*; value objects are immutable"
    with pytest.raises(ImmutabilityException, match=regex_match):
        my_instance.x = 15
    with pytest.raises(ImmutabilityException, match=regex_match):
        my_instance.y = 20


def test_value_object_decorator_hash_single_attribute():
    @value_object
    class MyClass:
        def __init__(self, x):
            self.x = x

    # Test that the decorated class has overridden hash method for a
    # single attribute
    my_instance = MyClass(5)
    other_instance = MyClass(5)
    assert hash(my_instance) == hash(other_instance)


def test_value_object_decorator_dataclass_initialization():
    @value_object()
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass can be instantiated with the
    # correct attributes
    my_instance = MyClass(x=5, y=10)
    assert my_instance.x == 5
    assert my_instance.y == 10


def test_value_object_decorator_dataclass_immutability():
    @value_object
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass is immutable
    my_instance = MyClass(5, 10)
    with pytest.raises(AttributeError):
        my_instance.x = 15
    with pytest.raises(AttributeError):
        my_instance.y = 20


def test_value_object_decorator_dataclass_hash():
    @value_object()
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass has overridden hash method
    # correctly
    my_instance = MyClass(x=5, y=10)
    other_instance = MyClass(5, 10)
    assert hash(my_instance) == hash(other_instance)


def test_value_object_decorator_dataclass_initialization_with_dataclass():
    @value_object
    @dataclass
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass can be instantiated with the
    # correct attributes
    my_instance = MyClass(5, 10)
    assert my_instance.x == 5
    assert my_instance.y == 10


def test_value_object_decorator_dataclass_immutability_with_dataclass():
    @value_object
    @dataclass
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass is immutable
    my_instance = MyClass(5, 10)
    regex_match = "Cannot modify .*; value objects are immutable"
    with pytest.raises(AttributeError, match=regex_match):
        my_instance.x = 15
    with pytest.raises(AttributeError, match=regex_match):
        my_instance.y = 20


def test_value_object_decorator_dataclass_hash_with_dataclass():
    @value_object
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass has overridden hash method
    # correctly
    my_instance = MyClass(x=5, y=10)
    other_instance = MyClass(5, 10)
    assert hash(my_instance) == hash(other_instance)


def test_value_object_decorator_equality():
    @value_object
    class MyClass:
        def __init__(self, x):
            self.x = x

    # Test that two instances with the same attribute values are equal
    my_instance = MyClass(5)
    other_instance = MyClass(5)
    assert my_instance == other_instance


def test_value_object_decorator_inequality():
    @value_object
    class MyClass:
        def __init__(self, x):
            self.x = x

    # Test that two instances with different attribute values are not
    # equal
    my_instance = MyClass(5)
    other_instance = MyClass(10)
    assert my_instance != other_instance


def test_value_object_decorator_exception_message():
    @value_object
    class MyClass:
        def __init__(self, x):
            self.x = x

    # Test that the correct exception message is displayed when trying
    # to modify an attribute
    my_instance = MyClass(5)
    regex_match = "Cannot modify .*; value objects are immutable"
    with pytest.raises(ImmutabilityException, match=regex_match):
        my_instance.x = 10
