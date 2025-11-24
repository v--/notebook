import pytest

from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..parsing import parse_formula
from ..signature import FormalLogicSignature
from .prenex import (
    DisallowedFormulaError,
    is_formula_in_pnf,
    is_formula_quantifierless,
    move_negations,
    move_quantifiers,
    remove_conditionals,
    formula_to_pnf,
)


@pytest_parametrize_lists(
    formula=[
        '⊤',
        '(x = y)',
        '((x = y) ∨ ¬(x = y))',
    ]
)
def test_is_formula_quantifierless_success(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert is_formula_quantifierless(parse_formula(formula, dummy_signature))


@pytest_parametrize_lists(
    formula=[
        '∀x.p¹(y)',
        '¬∀x.p¹(y)',
    ]
)
def test_is_formula_quantifierless_failure(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert not is_formula_quantifierless(parse_formula(formula, dummy_signature))


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


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',                expected='(x = y)'),
    dict(formula='(p¹(x) ∨ q¹(y))',        expected='(p¹(x) ∨ q¹(y))'),
    dict(formula='(p¹(x) → q¹(y))',        expected='(¬p¹(x) ∨ q¹(y))'),
    dict(formula='(p¹(x) ↔ q¹(y))',        expected='((¬p¹(x) ∨ q¹(y)) ∧ (p¹(x) ∨ ¬q¹(y)))'),
    dict(formula='¬(p¹(x) → q¹(y))',       expected='¬(¬p¹(x) ∨ q¹(y))'),
    dict(formula='∀y.∃z.¬(p¹(x) → q¹(y))', expected='∀y.∃z.¬(¬p¹(x) ∨ q¹(y))')
)
def test_remove_conditionals_success(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(remove_conditionals(parse_formula(formula, dummy_signature))) == expected


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',                expected='(x = y)'),
    dict(formula='(p¹(x) ∨ q¹(y))',        expected='(p¹(x) ∨ q¹(y))'),
    dict(formula='(p¹(x) → q¹(y))',        expected='(¬p¹(x) ∨ q¹(y))'),
    dict(formula='(p¹(x) ↔ q¹(y))',        expected='((¬p¹(x) ∨ q¹(y)) ∧ (p¹(x) ∨ ¬q¹(y)))'),
    dict(formula='¬(p¹(x) → q¹(y))',       expected='¬(¬p¹(x) ∨ q¹(y))'),
    dict(formula='∀y.∃z.¬(p¹(x) → q¹(y))', expected='∀y.∃z.¬(¬p¹(x) ∨ q¹(y))')
)
def test_move_negations_success(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(remove_conditionals(parse_formula(formula, dummy_signature))) == expected


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',           expected='(x = y)'),
    dict(formula='¬(x = y)',          expected='¬(x = y)'),
    dict(formula='¬¬(x = y)',         expected='(x = y)'),
    dict(formula='¬(p¹(x) ∨ ¬q¹(y))', expected='(¬p¹(x) ∧ q¹(y))'),
    dict(
        formula='¬∀y.∃z.(p¹(x) ∨ ¬q¹(y))',
        expected='∃y.∀z.(¬p¹(x) ∧ q¹(y))'
    ),
    dict(
        formula='¬(p¹(x) ∨ ¬(q¹(y) ∧ ¬(∃z.r¹(z) ∨ ¬s⁰)))',
        expected='(¬p¹(x) ∧ (q¹(y) ∧ (∀z.¬r¹(z) ∧ s⁰)))'
    )
)
def test_move_negations(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(move_negations(parse_formula(formula, dummy_signature))) == expected


def test_move_negations_conditional(dummy_signature: FormalLogicSignature) -> None:
    formula = parse_formula('¬(p¹(x) → p¹(y))', dummy_signature)

    with pytest.raises(DisallowedFormulaError) as excinfo:
        move_negations(formula)

    assert str(excinfo.value) == 'Unexpected connective →'


def test_move_negations_biconditional(dummy_signature: FormalLogicSignature) -> None:
    formula = parse_formula('¬(p¹(x) ↔ p¹(y))', dummy_signature)

    with pytest.raises(DisallowedFormulaError) as excinfo:
        move_negations(formula)

    assert str(excinfo.value) == 'Unexpected connective ↔'


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',     expected='(x = y)'),
    dict(formula='∀y.p¹(x)',    expected='∀y.p¹(x)'),
    dict(formula='∀y.∀y.p¹(x)', expected='∀y.∀y.p¹(x)'),
    dict(formula='∀y.∀y.p¹(y)', expected='∀y.∀y.p¹(y)'),
    dict(formula='(∀x.p¹(x) ∨ q¹(y))', expected='∀x.(p¹(x) ∨ q¹(y))'),
    dict(formula='(∀x.p¹(x) ∨ q¹(x))', expected='∀a.(p¹(a) ∨ q¹(x))'),
    dict(formula='(∀x.p¹(x) ∨ q²(a, x))', expected='∀b.(p¹(b) ∨ q²(a, x))'),
    dict(
        formula='(∀x.p¹(x) ∨ ∀x.q¹(x))',
        expected='∀x.∀a.(p¹(x) ∨ q¹(a))'
    ),
    dict(
        formula='((∃x.p¹(x) ∧ ∃y.q¹(y)) ∨ (∃x.p¹(x) ∧ ∃y.q¹(y)))',
        expected='∃x.∃y.∃a.∃b.((p¹(x) ∧ q¹(y)) ∨ (p¹(a) ∧ q¹(b)))'
    ),
    dict(
        formula='((∀x.p¹(x) ∨ q¹(x)) ∧ ∃a.r¹(a))',
        expected='∃a.∀b.((p¹(b) ∨ q¹(x)) ∧ r¹(a))'
    ),
)
def test_move_quantifiers(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(move_quantifiers(parse_formula(formula, dummy_signature))) == expected


def test_move_quantifiers_conditional(dummy_signature: FormalLogicSignature) -> None:
    formula = parse_formula('¬(p¹(x) → p¹(y))', dummy_signature)

    with pytest.raises(DisallowedFormulaError) as excinfo:
        move_quantifiers(formula)

    assert str(excinfo.value) == 'Unexpected connective →'


def test_move_quantifiers_biconditional(dummy_signature: FormalLogicSignature) -> None:
    formula = parse_formula('¬(p¹(x) ↔ p¹(y))', dummy_signature)

    with pytest.raises(DisallowedFormulaError) as excinfo:
        move_quantifiers(formula)

    assert str(excinfo.value) == 'Unexpected connective ↔'



@pytest_parametrize_kwargs(
    dict(formula='(x = y)',   expected='(x = y)'),
    dict(formula='¬∀y.p¹(x)', expected='∃y.¬p¹(x)'),
    dict(
        formula='((∀x.p¹(x) ∨ q¹(x)) ∧ ∃x.¬¬r¹(x))',
        expected='∃a.∀b.((p¹(b) ∨ q¹(x)) ∧ r¹(a))'
    ),
    dict(
        formula='((∃x.¬p¹(x) → q¹(x)) ∧ ∃x.r¹(b))',
        expected='∃a.∀a.((p¹(a) ∨ q¹(x)) ∧ r¹(b))'
    ),
)
def test_formula_to_pnf(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    pnf = formula_to_pnf(parse_formula(formula, dummy_signature))
    assert is_formula_in_pnf(pnf)
    assert str(pnf) == expected
