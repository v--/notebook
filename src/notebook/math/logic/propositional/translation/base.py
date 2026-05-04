from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .exceptions import UnspecifiedReplacementError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from notebook.math.logic.formulas import Formula
    from notebook.math.logic.propositional.formulas import PropVariable


@dataclass(frozen=True)
class PropFormulaTranslation:
    mapping: Mapping[PropVariable, Formula] = field(default_factory=dict)

    def translate_variable(self, var: PropVariable) -> Formula:
        try:
            return self.mapping[var]
        except KeyError:
            raise UnspecifiedReplacementError(f'No translation specified for propositional variable {var.symbol}') from None

        return self.mapping.get(var, var)
