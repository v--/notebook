from .formulas import Formula, QuantifierFormula
from .pnf import PNFVerificationVisitor


class SNFVerificationVisitor(PNFVerificationVisitor):
    def visit_quantifier(self, formula: QuantifierFormula) -> bool:
        return formula.quantifier == '∀' and self.visit(formula.sub)


def is_formula_in_snf(formula: Formula) -> bool:
    return SNFVerificationVisitor().visit(formula)
