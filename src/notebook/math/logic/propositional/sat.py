from itertools import product
from typing import no_type_check
lazy from collections.abc import Iterable, Sequence

from notebook.support.coderefs import collector

from .evaluation import evaluate_prop_formula
from .interpretation import PropInterpretation
from .variables import get_prop_variables
lazy from .formulas import PropFormula, PropVariable


def iter_interpretations_for_variables(variables: Sequence[PropVariable]) -> Iterable[PropInterpretation]:
    for spec in product([True, False], repeat=len(variables)):
        yield PropInterpretation(dict(zip(variables, spec, strict=True)))


@no_type_check  # mypy does not yet support comprehension unpacking; see https://github.com/python/mypy/issues/21447
def iter_interpretations(*formulas: PropFormula) -> Iterable[PropInterpretation]:
    return iter_interpretations_for_variables(
        sorted(*get_prop_variables(formula) for formula in formulas),
    )


@collector.ref('alg:brute_force_propositional_satisfaction')
def brute_force_satisfy(formula: PropFormula) -> PropInterpretation | None:
    for interp in iter_interpretations(formula):
        if evaluate_prop_formula(formula, interp):
            return interp

    return None


def is_tautology(formula: PropFormula) -> bool:
    return all(
        evaluate_prop_formula(formula, interp)
        for interp in iter_interpretations(formula)
    )


def is_contradiction(formula: PropFormula) -> bool:
    return all(
        not evaluate_prop_formula(formula, interp)
        for interp in iter_interpretations(formula)
    )


def are_semantically_equivalent(first: PropFormula, second: PropFormula) -> bool:
    return all(
        evaluate_prop_formula(first, interp) == evaluate_prop_formula(second, interp)
        for interp in iter_interpretations(first, second)
    )


def are_equisatisfiable(first: PropFormula, second: PropFormula) -> bool:
    model_first = brute_force_satisfy(first)
    model_second = brute_force_satisfy(second)
    return (model_first is None) == (model_second is None)
