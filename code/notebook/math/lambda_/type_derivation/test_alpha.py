import re
from collections.abc import Mapping

import pytest

from ....support.pytest import pytest_parametrize_kwargs
from ..parsing import parse_term, parse_type, parse_variable
from ..signature import LambdaSignature
from ..typing import TypingStyle
from .alpha import alpha_convert_derivation
from .exceptions import TypeDerivationError
from .inference import derive_type


@pytest_parametrize_kwargs(
    dict(m='x', n='x', context={'x': 'τ'}),
    dict(m='(fx)', n='(fx)', context={'f': '(τ → τ)', 'x': 'τ'}),
    dict(m='(λx:τ.x)', n='(λx:τ.x)', context={}),
    dict(m='(λx:τ.x)', n='(λy:τ.y)', context={}),
    dict(
        m='(λx:(τ → σ).(λy:τ.(xy)))',
        n='(λa:(τ → σ).(λb:τ.(ab)))',
        context={}
    ),
)
def test_alpha_convert_derivation_success(m: str, n: str, context: Mapping[str, str], dummy_signature: LambdaSignature) -> None:
    tree = derive_type(
        parse_term(dummy_signature, m, TypingStyle.explicit),
        {
            parse_variable(var): parse_type(dummy_signature, type_)
            for var, type_ in context.items()
        }
    )

    equivalent_term = parse_term(dummy_signature, n, TypingStyle.explicit)
    assert alpha_convert_derivation(tree, equivalent_term).conclusion.term == equivalent_term


@pytest_parametrize_kwargs(
    dict(m='x', n='y', context={'x': 'τ'}),
    dict(m='(λx:τ.x)', n='(λx:σ.x)', context={}),
    dict(m='(λx:τ.x)', n='(λx:τ.y)', context={}),
    dict(
        m='(λx:(τ → σ).(λy:τ.(xy)))',
        n='(λa:(τ → σ).(λa:τ.(aa)))',
        context={}
    ),
)
def test_alpha_convert_derivation_failure(m: str, n: str, context: Mapping[str, str], dummy_signature: LambdaSignature) -> None:
    tree = derive_type(
        parse_term(dummy_signature, m, TypingStyle.explicit),
        {
            parse_variable(var): parse_type(dummy_signature, type_)
            for var, type_ in context.items()
        }
    )

    equivalent_term = parse_term(dummy_signature, n, TypingStyle.explicit)

    with pytest.raises(TypeDerivationError, match=f'The terms {re.escape(m)} and {re.escape(n)} are not α-equivalent'):
        alpha_convert_derivation(tree, equivalent_term)
