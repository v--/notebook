from ...alphabet import Quantifier
from ...formulas import Formula, QuantifierFormula
from ..prenex.validation import PNFValidationVisitor


class SNFValidationVisitor(PNFValidationVisitor):
    def visit_quantifierifier(self, formula: QuantifierFormula) -> bool:
        return formula.quant == Quantifier.UNIVERSAL and self.visit(formula.body)


def is_formula_in_snf(formula: Formula) -> bool:
    return SNFValidationVisitor().visit(formula)
