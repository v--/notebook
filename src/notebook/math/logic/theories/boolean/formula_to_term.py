from typing import TYPE_CHECKING, cast, override

from notebook.math.logic.parsing import parse_variable
from notebook.math.logic.propositional import (
    PropConnectiveFormula,
    PropFormula,
    PropFormulaVisitor,
    PropNegationFormula,
    PropVariable,
)
from notebook.math.logic.terms import FunctionApplication, Term
from notebook.math.logic.theories.exceptions import UnrecognizedSymbolError
from notebook.support.coderefs import collector

from .signature import (
    BOOLEAN_ALGEBRA_SIGNATURE,
    FORMULA_CONNECTIVE_TO_TERM_CONNECTIVE,
    FORMULA_CONSTANT_TO_TERM_CONSTANT,
)


if TYPE_CHECKING:
    from notebook.math.logic.alphabet import LatticeConnective
    from notebook.math.logic.formulas import PropConstant


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
            [self.visit(formula.body)],
        )

    @override
    def visit_connective(self, formula: PropConnectiveFormula) -> Term:
        if formula.conn not in FORMULA_CONNECTIVE_TO_TERM_CONNECTIVE:
            raise UnrecognizedSymbolError(f'Expected a Boolean algebra connective, but got {formula.conn}')

        return FunctionApplication(
            FORMULA_CONNECTIVE_TO_TERM_CONNECTIVE[cast('LatticeConnective', formula.conn)],
            [self.visit(formula.left), self.visit(formula.right)],
        )


@collector.ref('alg:propositional_formula_to_boolean_term')
def prop_formula_to_boolean_term(formula: PropFormula) -> Term:
    return FormulaToTermVisitor().visit(formula)
