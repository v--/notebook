from dataclasses import dataclass

from ..formulas import Formula, QuantifierFormula
from ..transformation import pull_quantifiers
from .prefix import QuantifierPrefix


@dataclass(frozen=True)
class PrenexFormula:
    prefix: QuantifierPrefix
    matrix: Formula

    def get_quantified(self) -> Formula:
        result = self.matrix

        for quant, var in reversed(list(self.prefix)):
            result = QuantifierFormula(quant, var, result)

        return result

    def __str__(self) -> str:
        return str(self.get_quantified())

    def is_universal(self) -> bool:
        return self.prefix.is_universal()

    def is_existential(self) -> bool:
        return self.prefix.is_existential()


# This is alg:fol_formula_to_prenex_normal_form in the monograph
def formula_to_prenex_form(formula: Formula) -> PrenexFormula:
    transformed = pull_quantifiers(formula)

    prefix = QuantifierPrefix()
    current = transformed

    while isinstance(current, QuantifierFormula):
        prefix.append(current.quant, current.var)
        current = current.body

    return PrenexFormula(prefix, current)
