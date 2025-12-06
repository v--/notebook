from typing import override

from ..formulas import Formula
from ..parsing import parse_formula
from .exceptions import PropositionalLogicError
from .formula_visitor import PropositionalFormulaVisitor
from .signature import PROPOSITIONAL_SIGNATURE
from .variables import PropositionalVariable


# The validation logic is part of the PropositionalFormulaVisitor
class PropositionalFormulaValidationVisitor[T](PropositionalFormulaVisitor[None]):
    @override
    def generic_visit(self, formula: Formula) -> None:
        return None


def parse_propositional_formula(source: str) -> Formula:
    formula = parse_formula(source, PROPOSITIONAL_SIGNATURE)
    PropositionalFormulaValidationVisitor().visit(formula)
    return formula


def parse_propositional_variable(source: str) -> PropositionalVariable:
    formula = parse_propositional_formula(source)

    if not isinstance(formula, PropositionalVariable):
        raise PropositionalLogicError(f'Encountered a propositional variable, but got {source}')

    return formula
