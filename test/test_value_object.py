from dataclasses import dataclass

import pytest

from dddpy.value_object import value_object


def test_value_object_decorator_initialization_single_attribute():
    @value_object
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


def test_value_object_decorator_immutability_multiple_attributes():
    @value_object
    class MyClass:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    # Test that the decorated class is immutable for multiple attributes
    my_instance = MyClass(5, 10)
    regex_match = "Cannot modify .*; value objects are immutable"
    with pytest.raises(AttributeError, match=regex_match):
        my_instance.x = 15
    with pytest.raises(AttributeError, match=regex_match):
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
    @value_object
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass can be instantiated with the
    # correct attributes
    my_instance = MyClass(5, 10)
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
    @value_object
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass has overridden hash method
    # correctly
    my_instance = MyClass(5, 10)
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
    @dataclass
    class MyClass:
        x: int
        y: int

    # Test that the decorated dataclass has overridden hash method
    # correctly
    my_instance = MyClass(5, 10)
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
    with pytest.raises(AttributeError, match=regex_match):
        my_instance.x = 10
