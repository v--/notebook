from dataclasses import dataclass, field
lazy from collections.abc import Mapping

lazy from notebook.math.logic.formulas import Formula
lazy from notebook.math.logic.propositional.formulas import PropVariable

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
