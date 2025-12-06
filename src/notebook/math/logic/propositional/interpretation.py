from collections.abc import Mapping
from dataclasses import dataclass, field

from .exceptions import MissingInterpretationError
from .formulas import PropositionalVariable
from .parsing import parse_propositional_variable


@dataclass(frozen=True)
class PropositionalInterpretation:
    mapping: Mapping[PropositionalVariable, bool] = field(default_factory=dict)

    @classmethod
    def infer(cls, **kwargs: bool) -> PropositionalInterpretation:
        return cls({ parse_propositional_variable(key): value for key, value in kwargs.items() })

    def get_value(self, var: PropositionalVariable) -> bool:
        if var in self.mapping:
            return self.mapping[var]

        raise MissingInterpretationError(f'No assignment specified for variable {var}')

    def modify(self, var: PropositionalVariable, value: bool) -> PropositionalInterpretation:  # noqa: FBT001
        return PropositionalInterpretation({**self.mapping, var: value})
