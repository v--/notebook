from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self

from ..alphabet import AuxImproperSymbol
from ..assertions import VariableTypeAssertion
from ..parsing import parse_variable
from ..variables import get_free_variables
from .exceptions import HolError


if TYPE_CHECKING:
    from collections.abc import Sequence

    from ..terms import TypedTerm
    from ..types import SimpleType


@dataclass
class HolExpression:
    term: TypedTerm
    type: SimpleType
    context: Sequence[VariableTypeAssertion] = field(default_factory=list)

    @classmethod
    def infer(cls, term: TypedTerm, type_: SimpleType, **kwargs: SimpleType) -> Self:
        return cls(
            term,
            type_,
            [VariableTypeAssertion(parse_variable(var), type_) for var, type_ in kwargs.items()],
        )

    def __post_init__(self) -> None:
        if get_free_variables(self.term) != {assertion.term for assertion in self.context}:
            raise HolError(f'Mismatch between free variables and context for HOL expression {self.term}')

    def __str__(self) -> str:
        context_str = ', '.join(map(str, self.context))
        return f'{context_str} {AuxImproperSymbol.SEQUENT} {self.term}: {self.type}'
