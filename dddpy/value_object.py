from dataclasses import dataclass
from typing import Any, Type, TypeVar

T = TypeVar('T')


class ValueObject:
    """
    A decorator class that enforces immutability and overrides
    equality methods.

    This class is used as a decorator for other classes to enforce
    immutability and override equality methods. It uses Python's
    dataclasses to create a new class with the same attributes but
    with added immutability and equality methods.

    Examples:
        @ValueObject
        class MyClassA:
            x: int
            y: str

            def __init__(self, x: int, y: str) -> None:
                self.x = x
                self.y = y

        my_instance = MyClass(5)
        my_instance.x = 10  # Raises AttributeError

    Warning:
        This class should only be used as a decorator for classes that
        do not have their own `__eq__` or `__hash__` methods.
    """

    def __init__(self, cls: Type[T]) -> None:
        """
        Initialize the ValueObject decorator.

        Args:
            cls (Type[T]): The class to be decorated.

        Returns:
            None
        """
        self.cls = dataclass(cls)
        self.enforce_immutability(cls)
        self.override_equality_methods(cls)

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """
        Call the decorated class with the given arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            T: An instance of the decorated class.
        """
        return self.cls(*args, **kwargs)

    @staticmethod
    def enforce_immutability(cls: Type[T]) -> None:
        """
        Enforce immutability on the decorated class.

        This method modifies the __setattr__ method of the decorated
        class to raise an AttributeError when trying to modify an
        existing attribute.

        Args:
            cls (Type[T]): The class to enforce immutability on.

        Returns:
            None
        """
        original_setattr = cls.__setattr__

        def new_setattr(instance: T, name: str, value: Any) -> None:
            if hasattr(instance, name):
                err_str = f"Cannot modify {name}; value objects are immutable"
                raise AttributeError(err_str)
            original_setattr(instance, name, value)

        cls.__setattr__ = new_setattr

    @staticmethod
    def override_equality_methods(cls: Type[T]) -> None:
        """
        Override the equality methods of the decorated class.

        This method adds __eq__ and __hash__ methods to the decorated
        class that compare and hash the sorted values of the
        instance's dictionary.

        Args:
            cls (Type[T]): The class to override equality methods on.

        Returns:
            None
        """
        def eq(inst: T, other: Any) -> bool:
            if not isinstance(other, inst.__class__):
                return False
            inst_values = sorted(inst.__dict__.values())
            other_values = sorted(other.__dict__.values())
            return inst_values == other_values

        cls.__eq__ = eq
        cls.__hash__ = lambda x: hash(tuple(x.__dict__.values()))


value_object = ValueObject
"""
Alias for the ValueObject class. This alias is more Pythonic for a decorator.

This class is used as a decorator for other classes to enforce
immutability and override equality methods. It uses Python's
dataclasses to create a new class with the same attributes but
with added immutability and equality methods.

Examples:
    @value_object
    class MyClassA:
        x: int
        y: str

        def __init__(self, x: int, y: str) -> None:
            self.x = x
            self.y = y

    my_instance = MyClass(5)
    my_instance.x = 10  # Raises AttributeError

Warning:
    This class should only be used as a decorator for classes that
    do not have their own `__eq__` or `__hash__` methods.
"""
