from dataclasses import dataclass
from typing import override

from ..formulas import Formula, FormulaTransformationVisitor, NegationFormula
from ..propositional import PropFormula, convert_to_prop_formula


@dataclass(frozen=True)
class CollapseRepeatedNegationVisitor(FormulaTransformationVisitor):
    @override
    def visit_negation(self, formula: NegationFormula) -> Formula:
        body = self.visit(formula.body)

        if isinstance(body, NegationFormula):
            return body.body

        return NegationFormula(body)


def collapse_repeated_negation(formula: Formula) -> Formula:
    return CollapseRepeatedNegationVisitor().visit(formula)


# This is alg:propositional_repeated_negation_collapse in the monograph
def collapse_repeated_negation_prop(formula: PropFormula) -> PropFormula:
    return convert_to_prop_formula(collapse_repeated_negation(formula))
