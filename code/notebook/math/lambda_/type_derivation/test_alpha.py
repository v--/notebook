import re

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from ..parsing import parse_term
from ..signature import LambdaSignature
from ..typing import TypingStyle
from .alpha import transform_derivation
from .exceptions import TypeDerivationError
from .inference import derive_type


@pytest_parametrize_kwargs(
    dict(m='(λx:τ.x)', n='(λx:τ.x)'),
    dict(m='(λx:τ.x)', n='(λy:τ.y)'),
    dict(
        m='(λx:(τ → σ).(λy:τ.(xy)))',
        n='(λa:(τ → σ).(λb:τ.(ab)))'
    ),
)
def test_transform_derivation_success(m: str, n: str, dummy_signature: LambdaSignature) -> None:
    tree = derive_type(
        parse_term(dummy_signature, m, TypingStyle.explicit)
    )

    equivalent_term = parse_term(dummy_signature, n, TypingStyle.explicit)
    assert transform_derivation(tree, equivalent_term).conclusion.term == equivalent_term


@pytest_parametrize_kwargs(
    dict(m='(λx:τ.x)', n='(λx:σ.x)'),
    dict(m='(λx:τ.x)', n='(λx:τ.(λy:σ.x))'),
    dict(
        m='(λx:(τ → σ).(λy:τ.(xy)))',
        n='(λa:(τ → σ).(λa:τ.(aa)))'
    ),
)
def test_transform_derivation_failure(m: str, n: str, dummy_signature: LambdaSignature) -> None:
    tree = derive_type(
        parse_term(dummy_signature, m, TypingStyle.explicit)
    )

    equivalent_term = parse_term(dummy_signature, n, TypingStyle.explicit)

    with pytest.raises(TypeDerivationError, match=f'The terms {re.escape(m)} and {re.escape(n)} are not α-equivalent'):
        transform_derivation(tree, equivalent_term)
