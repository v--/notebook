from collections.abc import Iterable
from itertools import product

from ..formulas import Formula
from .evaluation import evaluate_propositional_formula
from .interpretation import PropositionalInterpretation
from .variables import get_propositional_variables


def iter_interpretations(*formulas: Formula) -> Iterable[PropositionalInterpretation]:
    variables = sorted(var for formula in formulas for var in get_propositional_variables(formula))

    for spec in product([True, False], repeat=len(variables)):
        yield PropositionalInterpretation(dict(zip(variables, spec, strict=True)))


# This is thm:brute_force_propositional_satisfaction in the monograph
def brute_force_satisfy(formula: Formula) -> PropositionalInterpretation | None:
    for interp in iter_interpretations(formula):
        if evaluate_propositional_formula(formula, interp):
            return interp

    return None


def is_tautology(formula: Formula) -> bool:
    return all(
        evaluate_propositional_formula(formula, interp)
        for interp in iter_interpretations(formula)
    )


def is_contradiction(formula: Formula) -> bool:
    return all(
        not evaluate_propositional_formula(formula, interp)
        for interp in iter_interpretations(formula)
    )


def are_semantically_equivalent(first: Formula, second: Formula) -> bool:
    return all(
        evaluate_propositional_formula(first, interp) == evaluate_propositional_formula(second, interp)
        for interp in iter_interpretations(first, second)
    )


def are_equisatisfiable(first: Formula, second: Formula) -> bool:
    model_first = brute_force_satisfy(first)
    model_second = brute_force_satisfy(second)
    return (model_first is None) == (model_second is None)
