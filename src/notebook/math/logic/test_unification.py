from collections.abc import Mapping, Sequence

import pytest

from ...support.pytest import pytest_parametrize_kwargs
from .parsing import parse_equation, parse_term, parse_variable
from .signature import FormalLogicSignature
from .substitution import AtomicLogicSubstitution
from .unification import UnificationError, unify


@pytest_parametrize_kwargs(
    # ex:alg:first_order_unification/noop
    dict(
        system=['(x = x)'],
        unifier=dict()
    ),
    dict(
        system=['(x = y)'],
        unifier=dict(x='y')
    ),
    dict(
        system=['(fᶜ⁰ = x)'],
        unifier=dict(x='fᶜ⁰')
    ),
    dict(
        system=['(x = f¹(y))', '(y = fᶜ⁰)'],
        unifier=dict(x='f¹(fᶜ⁰)', y='fᶜ⁰')
    ),
    # ex:alg:first_order_unification/glue
    dict(
        system=['(x = f¹(y))', '(x = f¹(z))'],
        unifier=dict(x='f¹(z)', y='z')
    ),
    dict(
        system=['(x = f¹(y))', '(y = fᶜ⁰)'],
        unifier=dict(x='f¹(fᶜ⁰)', y='fᶜ⁰')
    ),
    # ex:alg:first_order_unification/418a
    dict(
        system=['(f²(x, y) = f²(g¹(fᶜ⁰), x))'],
        unifier=dict(x='g¹(fᶜ⁰)', y='g¹(fᶜ⁰)')
    ),
    # ex:alg:first_order_unification/418c
    dict(
        system=['(f²(x, fᶜ⁰) = f²(g¹(y), z))'],
        unifier=dict(x='g¹(y)', z='fᶜ⁰')
    ),
)
def test_unify(system: Sequence[str], unifier: Mapping[str, str], dummy_signature: FormalLogicSignature) -> None:
    system_ = [parse_equation(e, dummy_signature) for e in system]
    unifier_ = AtomicLogicSubstitution(
        variable_mapping={
            parse_variable(key): parse_term(value, dummy_signature) for key, value in unifier.items()
        }
    )

    result = unify(system_)
    assert result == unifier_


@pytest_parametrize_kwargs(
    dict(
        system=['(x = fᶜ⁰)', '(x = gᶜ⁰)'],
    ),
    # ex:alg:first_order_unification/loop
    dict(
        system=['(x = f¹(x))'],
    ),
    dict(
        system=['(f²(x, y) = g²(x, y))'],
    ),
    dict(
        system=['(x = f¹(y))', '(y = f¹(x))'],
    ),
    # ex:alg:first_order_unification/418b
    dict(
        system=['(f²(x, y) = f²(g¹(x), x))'],
    ),
    # ex:alg:first_order_unification/418d
    dict(
        system=['(f²(x, x) = f²(g¹(y), y))'],
    ),
)
def test_unify_fail(system: Sequence[str], dummy_signature: FormalLogicSignature) -> None:
    system_ = [parse_equation(e, dummy_signature) for e in system]

    with pytest.raises(UnificationError):
        unify(system_)
