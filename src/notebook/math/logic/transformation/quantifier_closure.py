from ..alphabet import Quantifier
from ..formulas import Formula, QuantifierFormula
from ..variables import get_formula_free_variables


def quantifier_closure(formula: Formula, quantifier: Quantifier) -> Formula:
    result = formula

    for var in get_formula_free_variables(formula):
        result = QuantifierFormula(quantifier, var, result)

    return result


def universal_closure(formula: Formula) -> Formula:
    return quantifier_closure(formula, Quantifier.UNIVERSAL)


def existential_closure(formula: Formula) -> Formula:
    return quantifier_closure(formula, Quantifier.EXISTENTIAL)

