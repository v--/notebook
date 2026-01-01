from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

from .exceptions import MissingInterpretationError
from .formulas import PropVariable
from .parsing import parse_prop_variable


@dataclass(frozen=True)
class PropInterpretation:
    mapping: Mapping[PropVariable, bool] = field(default_factory=dict)

    @classmethod
    def from_kwargs(cls, **kwargs: bool) -> PropInterpretation:
        return cls({ parse_prop_variable(key): value for key, value in kwargs.items() })

    def get_value(self, var: PropVariable) -> bool:
        if var in self.mapping:
            return self.mapping[var]

        raise MissingInterpretationError(f'No assignment specified for variable {var.symbol.name}')

    def modify(self, var: PropVariable, value: bool) -> PropInterpretation:  # noqa: FBT001
        return PropInterpretation({ **self.mapping, var: value })

    def get_dual(self) -> PropInterpretation:
        return PropInterpretation({ var: not value for var, value in self.mapping.items() })

    def iter_items(self) -> Iterable[tuple[PropVariable, bool]]:
        return self.mapping.items()

    def get_kwargs(self) -> Mapping[str, bool]:
        return {var.symbol.name: value for var, value in self.iter_items()}
