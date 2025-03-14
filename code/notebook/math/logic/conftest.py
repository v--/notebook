import pytest

from ...support.unicode import itoa_subscripts
from .signature import FormalLogicSignature


@pytest.fixture
def dummy_signature(max_args: int = 10) -> FormalLogicSignature:
    signature = FormalLogicSignature()

    for l in ['f', 'g', 'h', 't']:
        for i in range(max_args):
            signature.add_symbol('FUNCTION', name=l + itoa_subscripts(i), arity=i)

    for l in ['p', 'q', 'r', 's']:
        for i in range(max_args):
            signature.add_symbol('PREDICATE', name=l + itoa_subscripts(i), arity=i)

    return signature
