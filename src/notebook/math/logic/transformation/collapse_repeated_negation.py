from dataclasses import dataclass
from typing import override

from notebook.math.logic.formulas import Formula, FormulaTransformationVisitor, NegationFormula
from notebook.math.logic.propositional import PropFormula, convert_to_prop_formula
from notebook.support.coderefs import collector


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


@collector.ref('alg:propositional_repeated_negation_collapse')
def collapse_repeated_negation_prop(formula: PropFormula) -> PropFormula:
    return convert_to_prop_formula(collapse_repeated_negation(formula))
