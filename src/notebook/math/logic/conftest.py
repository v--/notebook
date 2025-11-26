import pytest

from ...support.unicode import itoa_superscripts
from .signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol


@pytest.fixture
def dummy_signature(max_args: int = 3) -> FormalLogicSignature:
    signature = FormalLogicSignature(
        FunctionSymbol(name='+', arity=2, infix=True),
        FunctionSymbol(name='×', arity=2, infix=True),
        PredicateSymbol(name='<', arity=2, infix=True),
        PredicateSymbol(name='>', arity=2, infix=True),
    )

    for char in ['f', 'g', 'h', 't']:
        for i in range(max_args + 1):
            signature.add_symbol(FunctionSymbol(name=char + itoa_superscripts(i), arity=i, infix=False))

    for char in ['p', 'q', 'r', 's']:
        for i in range(max_args + 1):
            signature.add_symbol(PredicateSymbol(name=char + itoa_superscripts(i), arity=i, infix=False))

    return signature
