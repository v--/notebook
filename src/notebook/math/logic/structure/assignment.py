from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..parsing import parse_variable
from .exceptions import MissingInterpretationError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from ..terms import Variable


@dataclass(frozen=True)
class VariableAssignment[T]:
    mapping: Mapping[Variable, T] = field(default_factory=dict)

    @classmethod
    def infer(cls, **kwargs: T) -> VariableAssignment:
        return cls({ parse_variable(key): value for key, value in kwargs.items() })

    def get_value(self, var: Variable) -> T:
        if var in self.mapping:
            return self.mapping[var]

        raise MissingInterpretationError(f'No assignment specified for variable {var.identifier}')

    def modify(self, var: Variable, value: T) -> VariableAssignment[T]:
        return VariableAssignment({**self.mapping, var: value})
