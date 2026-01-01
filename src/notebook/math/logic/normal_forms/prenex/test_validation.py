from .....support.pytest import pytest_parametrize_lists
from ...parsing import parse_formula
from ...signature import FormalLogicSignature
from .validation import (
    is_formula_in_pnf,
)


@pytest_parametrize_lists(
    formula=[
        '(x = y)',
        '∀x.p¹(y)',
        '∀z.∃z.(¬r¹(y) ∧ ¬r²(z, y))',
    ]
)
def test_is_formula_in_pnf_success(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert is_formula_in_pnf(parse_formula(formula, dummy_signature))


@pytest_parametrize_lists(
    formula=[
        '¬∀x.p¹(y)',
        '∀y.∃z.(¬p¹(z) ∧ ∀x.(q²(z, x) → ¬r²(y, x)))',
    ]
)
def test_is_formula_in_pnf_failure(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert not is_formula_in_pnf(parse_formula(formula, dummy_signature))

