from collections.abc import Mapping
from dataclasses import dataclass, field

from ...formulas import Formula
from ..formulas import PropVariable
from .exceptions import UnspecifiedReplacementError


@dataclass(frozen=True)
class PropFormulaTranslation:
    mapping: Mapping[PropVariable, Formula] = field(default_factory=dict)

    def translate_variable(self, var: PropVariable) -> Formula:
        try:
            return self.mapping[var]
        except KeyError:
            raise UnspecifiedReplacementError(f'No translation specified for propositional variable {var.symbol}') from None

        return self.mapping.get(var, var)
