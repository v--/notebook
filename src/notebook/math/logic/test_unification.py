from typing import TYPE_CHECKING

import pytest

from notebook.support.coderefs import collector
from notebook.support.pytest import pytest_parametrize_kwargs

from .parsing import parse_equation, parse_term, parse_variable
from .substitution import AtomicLogicSubstitution
from .unification import UnificationError, unify


if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from .signature import FormalLogicSignature


@pytest_parametrize_kwargs(
    collector.ref_proxy('ex:alg:first_order_unification/noop',
        system=['(x = x)'],
        unifier={},
    ),
    dict(
        system=['(x = y)'],
        unifier=dict(x='y'),
    ),
    dict(
        system=['(f⁰ = x)'],
        unifier=dict(x='f⁰'),
    ),
    dict(
        system=['(x = f¹(y))', '(y = f⁰)'],
        unifier=dict(x='f¹(f⁰)', y='f⁰'),
    ),
    collector.ref_proxy('ex:alg:first_order_unification/glue',
        system=['(x = f¹(y))', '(x = f¹(z))'],
        unifier=dict(x='f¹(z)', y='z'),
    ),
    dict(
        system=['(x = f¹(y))', '(y = f⁰)'],
        unifier=dict(x='f¹(f⁰)', y='f⁰'),
    ),
    collector.ref_proxy('ex:alg:first_order_unification/418a',
        system=['(f²(x, y) = f²(g¹(f⁰), x))'],
        unifier=dict(x='g¹(f⁰)', y='g¹(f⁰)'),
    ),
    collector.ref_proxy('ex:alg:first_order_unification/418c',
        system=['(f²(x, f⁰) = f²(g¹(y), z))'],
        unifier=dict(x='g¹(y)', z='f⁰'),
    ),
)
def test_unify(system: Sequence[str], unifier: Mapping[str, str], dummy_signature: FormalLogicSignature) -> None:
    system_ = [parse_equation(e, dummy_signature) for e in system]
    unifier_ = AtomicLogicSubstitution(
        variable_mapping={
            parse_variable(key): parse_term(value, dummy_signature) for key, value in unifier.items()
        },
    )

    result = unify(system_)
    assert result == unifier_


@pytest_parametrize_kwargs(
    dict(
        system=['(x = f⁰)', '(x = g⁰)'],
    ),
    collector.ref_proxy('ex:alg:first_order_unification/loop',
        system=['(x = f¹(x))'],
    ),
    dict(
        system=['(f²(x, y) = g²(x, y))'],
    ),
    dict(
        system=['(x = f¹(y))', '(y = f¹(x))'],
    ),
    collector.ref_proxy('ex:alg:first_order_unification/418b',
        system=['(f²(x, y) = f²(g¹(x), x))'],
    ),
    collector.ref_proxy('ex:alg:first_order_unification/418d',
        system=['(f²(x, x) = f²(g¹(y), y))'],
    ),
)
def test_unify_fail(system: Sequence[str], dummy_signature: FormalLogicSignature) -> None:
    system_ = [parse_equation(e, dummy_signature) for e in system]

    with pytest.raises(UnificationError):
        unify(system_)
