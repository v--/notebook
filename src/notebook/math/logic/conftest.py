import pytest

from ...support.unicode import itoa_superscripts
from .signature import FormalLogicSignature


@pytest.fixture
def dummy_signature(max_args: int = 3) -> FormalLogicSignature:
    signature = FormalLogicSignature()

    for char in ['+', '×']:
        signature.add_symbol('FUNCTION', name=char, arity=2, infix=True)

    for char in ['<', '>']:
        signature.add_symbol('PREDICATE', name=char, arity=2, infix=True)

    for char in ['f', 'g', 'h', 't']:
        for i in range(max_args + 1):
            signature.add_symbol('FUNCTION', name=char + itoa_superscripts(i), arity=i, infix=False)

    for char in ['p', 'q', 'r', 's']:
        for i in range(max_args + 1):
            signature.add_symbol('PREDICATE', name=char + itoa_superscripts(i), arity=i, infix=False)

    return signature
