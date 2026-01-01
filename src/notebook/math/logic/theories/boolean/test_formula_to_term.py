from .....support.pytest import pytest_parametrize_kwargs
from ...parsing import parse_term, parse_variable
from ...propositional import evaluate_prop_formula, iter_interpretations, parse_prop_formula
from ...structure import VariableAssignment, evaluate_term
from .formula_to_term import prop_formula_to_boolean_term
from .signature import BOOLEAN_ALGEBRA_SIGNATURE
from .term_to_formula import boolean_term_to_prop_formula
from .two_element import TwoElementBooleanAlgebra


@pytest_parametrize_kwargs(
    dict(formula='⊤',       term='⫪'),
    dict(formula='p',       term='p'),
    dict(formula='¬p',      term='⫬p'),
    dict(formula='(p ∧ q)', term='(p ⩓ q)'),
    dict(formula='(p ∨ q)', term='(p ⩔ q)'),
    dict(formula='((p ∨ ¬q) ∧ ¬(q ∨ p))', term='((p ⩔ ⫬q) ⩓ ⫬(q ⩔ p))'),
)
def test_dualize_formula_prop(formula: str, term: str) -> None:
    formula_ = parse_prop_formula(formula)
    term_ = parse_term(term, BOOLEAN_ALGEBRA_SIGNATURE)

    for prop_interp in iter_interpretations(formula_):
        fol_structure = TwoElementBooleanAlgebra()
        fol_assignment = VariableAssignment({
            parse_variable(var.symbol.name): value for var, value in prop_interp.mapping.items()
        })

        assert evaluate_prop_formula(formula_, prop_interp) == evaluate_term(term_, fol_structure, fol_assignment)

    assert prop_formula_to_boolean_term(formula_) == term_
    assert formula_ == boolean_term_to_prop_formula(term_)
