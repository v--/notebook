from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from notebook.math.lambda_.alphabet import AuxImproperSymbol
from notebook.math.lambda_.type_context import TypeContext
from notebook.math.lambda_.variables import get_free_variables
from notebook.support.iteration import string_accumulator

from .exceptions import HolError


if TYPE_CHECKING:
    from collections.abc import Iterable

    from notebook.math.lambda_.terms import TypedTerm
    from notebook.math.lambda_.types import SimpleType


@dataclass
class HolExpression:
    term: TypedTerm
    type: SimpleType
    context: TypeContext = field(default_factory=TypeContext)

    def __post_init__(self) -> None:
        if get_free_variables(self.term) != set(self.context.keys()):
            raise HolError(f'Mismatch between free variables and context for HOL expression {self.term}')

    @string_accumulator()
    def __str__(self) -> Iterable[str]:  # noqa: PLE0307
        for i, (var, type_) in enumerate(self.context.items()):
            if i > 0:
                yield ','

            yield f'{var}: {type_}'

        yield f'{AuxImproperSymbol.SEQUENT} {self.term}: {self.type}'
