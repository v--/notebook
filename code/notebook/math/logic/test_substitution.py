from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_formula, parse_term
from .signature import FormalLogicSignature
from .substitution import substitute_in_formula, substitute_in_term


@pytest_parametrize_kwargs(
    dict(
        term='x',
        from_='x', to='y',
        expected='y'
    ),
    dict(
        term='y',
        from_='x', to='z',
        expected='y'
    ),
    dict(
        term='f₁(x)',
        from_='x', to='y',
        expected='f₁(y)'
    ),
    dict(
        term='f₂(g₁(x), h₁(g₁(x)))',
        from_='g₁(x)', to='y',
        expected='f₂(y, h₁(y))'
    )
)
def test_substitute_in_term(term: str, from_: str, to: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    actual = str(
        substitute_in_term(
            parse_term(dummy_signature, term),
            parse_term(dummy_signature, from_),
            parse_term(dummy_signature, to)
        )
    )

    assert actual == expected


@pytest_parametrize_kwargs(
    # Straighforward substitution
    dict(
        formula='p₁(x)',
        from_='x', to='y',
        expected='p₁(y)'
    ),
    dict(
        formula='p₁(y)',
        from_='x', to='z',
        expected='p₁(y)'
    ),
    dict(
        formula='(g₁(x) = h₁(g₁(x)))',
        from_='g₁(x)', to='y',
        expected='(y = h₁(y))'
    ),
    # (Avoiding) capturing free variables
    dict(
        formula='∀x.p₁(y)',
        from_='y', to='z',
        expected='∀x.p₁(z)'
    ),
    dict(
        formula='∀x.p₁(y)',
        from_='y', to='x',
        expected='∀a.p₁(x)'
    ),
    dict(
        formula='∀x.p₂(x, y)',
        from_='y', to='x',
        expected='∀a.p₂(a, x)'
    ),
    # (Avoiding) colliding variables
    dict(
        formula='∀x.p₁(y)',
        from_='y', to='x',
        expected='∀a.p₁(x)'
    ),
)
def test_substitute_in_formula(formula: str, from_: str, to: str, expected: str, dummy_signature: FormalLogicSignature) -> None:
    actual = str(
        substitute_in_formula(
            parse_formula(dummy_signature, formula),
            parse_term(dummy_signature, from_),
            parse_term(dummy_signature, to)
        )
    )

    assert actual == expected
