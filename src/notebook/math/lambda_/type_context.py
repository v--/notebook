from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING

from ...support.iteration import string_accumulator
from .parsing import parse_variable
from .terms import Variable
from .types import SimpleType


if TYPE_CHECKING:
    from collections.abc import Iterable

    from .assertions import VariableTypeAssertion


class TypeContext(Mapping[Variable, SimpleType]):
    mapping: Mapping[Variable, SimpleType]

    @classmethod
    def infer(cls, *args: VariableTypeAssertion, **kwargs: SimpleType) -> TypeContext:
        return TypeContext(
            {
                parse_variable(var_name): type_ for var_name, type_ in kwargs.items()
            } | {
                assertion.term: assertion.type for assertion in args
            },
        )

    def __init__(self, mapping: Mapping[Variable, SimpleType] = {}) -> None:
        self.mapping = mapping

    def modify(self, var: Variable, type_: SimpleType) -> TypeContext:
        return TypeContext({**self.mapping, var: type_})

    @string_accumulator()
    def __str__(self) -> Iterable[str]:  # noqa: PLE0307
        for i, (var, type_) in enumerate(self.mapping.items()):
            if i > 0:
                yield ','

            yield f'{var}: {type_}'

    def __getitem__(self, key: str | Variable) -> SimpleType:
        actual_key = parse_variable(key) if isinstance(key, str) else key
        return self.mapping[actual_key]

    def __contains__(self, key: object) -> bool:
        actual_key = parse_variable(key) if isinstance(key, str) else key
        return actual_key in self.mapping

    def __len__(self) -> int:
        return len(self.mapping)

    def __iter__(self) -> Iterator[Variable]:
        return iter(self.mapping)


EMPTY_CONTEXT = TypeContext()
