from dataclasses import dataclass

from notebook.math.logic.formulas import Formula, QuantifierFormula
from notebook.math.logic.transformation import pull_quantifiers
from notebook.support.coderefs import collector

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


@collector.ref('alg:fol_formula_to_prenex_normal_form')
def formula_to_prenex_form(formula: Formula) -> PrenexFormula:
    transformed = pull_quantifiers(formula)

    prefix = QuantifierPrefix()
    current = transformed

    while isinstance(current, QuantifierFormula):
        prefix.append(current.quant, current.var)
        current = current.body

    return PrenexFormula(prefix, current)
