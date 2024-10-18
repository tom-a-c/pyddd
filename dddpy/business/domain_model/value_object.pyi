# mymodule.pyi

from typing import Protocol, Callable, Any, TypeVar, Union

T = TypeVar('T', bound=Union[str, int, Any])

class SupportsDecoratorB(Protocol):
    @property
    def precondition(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        ...

class DynamicAttributesProtocol(Protocol):
    def __getattr__(self, name: str) -> Union[T, SupportsDecoratorB]:
        ...

# noinspection PyUnboundLocalVariable
def value_object(cls: type) -> DynamicAttributesProtocol:
    ...