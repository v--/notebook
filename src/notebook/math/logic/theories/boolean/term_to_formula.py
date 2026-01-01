from ...formulas import PropConstant
from ...propositional import (
    DEFAULT_PROP_SIGNATURE,
    PropConnectiveFormula,
    PropFormula,
    PropNegationFormula,
)
from ...terms import FunctionApplication, Term, Variable
from ..exceptions import UnrecognizedSymbolError
from .signature import (
    BOOLEAN_ALGEBRA_SIGNATURE,
    TERM_CONNECTIVE_TO_FORMULA_CONNECTIVE,
    TERM_CONSTANT_TO_FORMULA_CONSTANT,
)


# This is alg:propositional_formula_to_boolean_term in the monograph
def boolean_term_to_prop_formula(term: Term) -> PropFormula:
    match term:
        case Variable():
            return DEFAULT_PROP_SIGNATURE.get_prop_variable(str(term.identifier))

        case FunctionApplication():
            if term.symbol in TERM_CONSTANT_TO_FORMULA_CONSTANT:
                return PropConstant(TERM_CONSTANT_TO_FORMULA_CONSTANT[term.symbol])

            if term.symbol in TERM_CONNECTIVE_TO_FORMULA_CONNECTIVE:
                return PropConnectiveFormula(
                    TERM_CONNECTIVE_TO_FORMULA_CONNECTIVE[term.symbol],
                    boolean_term_to_prop_formula(term.arguments[0]),
                    boolean_term_to_prop_formula(term.arguments[1])
                )

            if term.symbol == BOOLEAN_ALGEBRA_SIGNATURE.get_function_symbol('⫬'):
                return PropNegationFormula(
                    boolean_term_to_prop_formula(term.arguments[0])
                )

            raise UnrecognizedSymbolError(f'Expected a Boolean algebra function symbol, but got {term.symbol}')
