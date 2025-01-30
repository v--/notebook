import pytest

from ...support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from .parsing import parse_formula
from .pnf import (
    PNFError,
    is_formula_in_pnf,
    is_formula_quantifierless,
    move_negations,
    move_quantifiers,
    remove_conditionals,
    to_pnf,
)
from .signature import FormalLogicSignature


@pytest_parametrize_lists(
    formula=[
        '⊤',
        '(x = y)',
        '((x = y) ∨ ¬(x = y))',
    ]
)
def test_is_formula_quantifierless_success(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert is_formula_quantifierless(parse_formula(dummy_signature, formula))


@pytest_parametrize_lists(
    formula=[
        '∀x.p₁(y)',
        '¬∀x.p₁(y)',
    ]
)
def test_is_formula_quantifierless_failure(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert not is_formula_quantifierless(parse_formula(dummy_signature, formula))


@pytest_parametrize_lists(
    formula=[
        '(x = y)',
        '∀x.p₁(y)',
        '∀z.∃z.(¬r₁(y) ∧ ¬r₂(z, y))',
    ]
)
def test_is_formula_in_pnf_success(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert is_formula_in_pnf(parse_formula(dummy_signature, formula))


@pytest_parametrize_lists(
    formula=[
        '¬∀x.p₁(y)',
        '∀y.∃z.(¬p₁(z) ∧ ∀x.(q₂(z, x) → ¬r₂(y, x)))',
    ]
)
def test_is_formula_in_pnf_failure(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert not is_formula_in_pnf(parse_formula(dummy_signature, formula))


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',                expected='(x = y)'),
    dict(formula='(p₁(x) ∨ q₁(y))',        expected='(p₁(x) ∨ q₁(y))'),
    dict(formula='(p₁(x) → q₁(y))',        expected='(¬p₁(x) ∨ q₁(y))'),
    dict(formula='(p₁(x) ↔ q₁(y))',        expected='((¬p₁(x) ∨ q₁(y)) ∧ (p₁(x) ∨ ¬q₁(y)))'),
    dict(formula='¬(p₁(x) → q₁(y))',       expected='¬(¬p₁(x) ∨ q₁(y))'),
    dict(formula='∀y.∃z.¬(p₁(x) → q₁(y))', expected='∀y.∃z.¬(¬p₁(x) ∨ q₁(y))')
)
def test_remove_conditionals_success(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(remove_conditionals(parse_formula(dummy_signature, formula))) == expected


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',                expected='(x = y)'),
    dict(formula='(p₁(x) ∨ q₁(y))',        expected='(p₁(x) ∨ q₁(y))'),
    dict(formula='(p₁(x) → q₁(y))',        expected='(¬p₁(x) ∨ q₁(y))'),
    dict(formula='(p₁(x) ↔ q₁(y))',        expected='((¬p₁(x) ∨ q₁(y)) ∧ (p₁(x) ∨ ¬q₁(y)))'),
    dict(formula='¬(p₁(x) → q₁(y))',       expected='¬(¬p₁(x) ∨ q₁(y))'),
    dict(formula='∀y.∃z.¬(p₁(x) → q₁(y))', expected='∀y.∃z.¬(¬p₁(x) ∨ q₁(y))')
)
def test_move_negations_success(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(remove_conditionals(parse_formula(dummy_signature, formula))) == expected


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',           expected='(x = y)'),
    dict(formula='¬(x = y)',          expected='¬(x = y)'),
    dict(formula='¬¬(x = y)',         expected='(x = y)'),
    dict(formula='¬(p₁(x) ∨ ¬q₁(y))', expected='(¬p₁(x) ∧ q₁(y))'),
    dict(
        formula='¬∀y.∃z.(p₁(x) ∨ ¬q₁(y))',
        expected='∃y.∀z.(¬p₁(x) ∧ q₁(y))'
    ),
    dict(
        formula='¬(p₁(x) ∨ ¬(q₁(y) ∧ ¬(∃z.r₁(z) ∨ ¬s₀)))',
        expected='(¬p₁(x) ∧ (q₁(y) ∧ (∀z.¬r₁(z) ∧ s₀)))'
    )
)
def test_move_negations(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(move_negations(parse_formula(dummy_signature, formula))) == expected


def test_move_negations_conditional(dummy_signature: FormalLogicSignature) -> None:
    formula = parse_formula(dummy_signature, '¬(p₁(x) → p₁(y))')

    with pytest.raises(PNFError) as excinfo:
        move_negations(formula)

    assert str(excinfo.value) == 'Unexpected connective →'


def test_move_negations_biconditional(dummy_signature: FormalLogicSignature) -> None:
    formula = parse_formula(dummy_signature, '¬(p₁(x) ↔ p₁(y))')

    with pytest.raises(PNFError) as excinfo:
        move_negations(formula)

    assert str(excinfo.value) == 'Unexpected connective ↔'


@pytest_parametrize_kwargs(
    dict(formula='(x = y)',     expected='(x = y)'),
    dict(formula='∀y.p₁(x)',    expected='∀y.p₁(x)'),
    dict(formula='∀y.∀y.p₁(x)', expected='∀y.∀y.p₁(x)'),
    dict(formula='∀y.∀y.p₁(y)', expected='∀y.∀y.p₁(y)'),
    dict(formula='(∀x.p₁(x) ∨ q₁(y))', expected='∀a.(p₁(a) ∨ q₁(y))'),
    dict(formula='(∀x.p₁(x) ∨ q₁(x))', expected='∀a.(p₁(a) ∨ q₁(x))'),
    dict(formula='(∀x.p₁(x) ∨ q₁(a))', expected='∀b.(p₁(b) ∨ q₁(a))'),
    dict(
        formula='(∀x.p₁(x) ∨ ∀x.q₁(x))',
        expected='∀a.∀b.(p₁(a) ∨ q₁(b))'
    ),
    dict(
        formula='((∃x.p₁(x) ∧ ∃y.q₁(y)) ∨ (∃x.p₁(x) ∧ ∃y.q₁(y)))',
        expected='∃b.∃a.∃c.∃d.((p₁(b) ∧ q₁(a)) ∨ (p₁(c) ∧ q₁(d)))'
    ),
    dict(
        formula='((∀x.p₁(x) ∨ q₁(x)) ∧ ∃a.r₁(a))',
        expected='∃b.∀c.((p₁(c) ∨ q₁(x)) ∧ r₁(b))'
    ),
)
def test_move_quantifiers(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(move_quantifiers(parse_formula(dummy_signature, formula))) == expected


def test_move_quantifiers_conditional(dummy_signature: FormalLogicSignature) -> None:
    formula = parse_formula(dummy_signature, '¬(p₁(x) → p₁(y))')

    with pytest.raises(PNFError) as excinfo:
        move_quantifiers(formula)

    assert str(excinfo.value) == 'Unexpected connective →'


def test_move_quantifiers_biconditional(dummy_signature: FormalLogicSignature) -> None:
    formula = parse_formula(dummy_signature, '¬(p₁(x) ↔ p₁(y))')

    with pytest.raises(PNFError) as excinfo:
        move_quantifiers(formula)

    assert str(excinfo.value) == 'Unexpected connective ↔'



@pytest_parametrize_kwargs(
    dict(formula='(x = y)',   expected='(x = y)'),
    dict(formula='¬∀y.p₁(x)', expected='∃y.¬p₁(x)'),
    dict(
        formula='((∀x.p₁(x) ∨ q₁(x)) ∧ ∃x.¬¬r₁(x))',
        expected='∃a.∀b.((p₁(b) ∨ q₁(x)) ∧ r₁(a))'
    ),
    dict(
        formula='((∃x.¬p₁(x) → q₁(x)) ∧ ∃x.r₁(b))',
        expected='∃a.∀c.((p₁(c) ∨ q₁(x)) ∧ r₁(b))'
    ),
)
def test_to_pnf(formula: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    pnf = to_pnf(parse_formula(dummy_signature, formula))
    assert is_formula_in_pnf(pnf)
    assert str(pnf) == expected
