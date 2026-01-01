from typing import cast, override

from ...alphabet import LatticeConnective
from ...formulas import PropConstant
from ...parsing import parse_variable
from ...propositional import (
    PropConnectiveFormula,
    PropFormula,
    PropFormulaVisitor,
    PropNegationFormula,
    PropVariable,
)
from ...terms import FunctionApplication, Term
from ..exceptions import UnrecognizedSymbolError
from .signature import (
    BOOLEAN_ALGEBRA_SIGNATURE,
    FORMULA_CONNECTIVE_TO_TERM_CONNECTIVE,
    FORMULA_CONSTANT_TO_TERM_CONSTANT,
)


class FormulaToTermVisitor(PropFormulaVisitor[Term]):
    @override
    def visit_prop_constant(self, formula: PropConstant) -> Term:
        return FunctionApplication(FORMULA_CONSTANT_TO_TERM_CONSTANT[formula.value], [])

    @override
    def visit_variable(self, formula: PropVariable) -> Term:
        return parse_variable(formula.symbol.name)

    @override
    def visit_negation(self, formula: PropNegationFormula) -> Term:
        return FunctionApplication(
            BOOLEAN_ALGEBRA_SIGNATURE.get_function_symbol('⫬'),
            [self.visit(formula.body)]
        )

    @override
    def visit_connective(self, formula: PropConnectiveFormula) -> Term:
        if formula.conn not in FORMULA_CONNECTIVE_TO_TERM_CONNECTIVE:
            raise UnrecognizedSymbolError(f'Expected a Boolean algebra connective, but got {formula.conn}')

        return FunctionApplication(
            FORMULA_CONNECTIVE_TO_TERM_CONNECTIVE[cast(LatticeConnective, formula.conn)],
            [self.visit(formula.left), self.visit(formula.right)]
        )


# This is alg:propositional_formula_to_boolean_term in the monograph
def prop_formula_to_boolean_term(formula: PropFormula) -> Term:
    return FormulaToTermVisitor().visit(formula)
