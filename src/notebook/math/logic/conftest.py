import pytest

from ...support.unicode import itoa_superscripts
from .signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol


@pytest.fixture
def dummy_signature(max_args: int = 3) -> FormalLogicSignature:
    signature = FormalLogicSignature(
        FunctionSymbol('∘', arity=2, notation='INFIX'),
        PredicateSymbol('≠', arity=2, notation='INFIX'),
    )

    for char in ['f', 'g', 'h', 't']:
        for i in range(max_args + 1):
            signature.add_symbol(FunctionSymbol(char + itoa_superscripts(i), arity=i))
            signature.add_symbol(FunctionSymbol(char + 'ᶜ' + itoa_superscripts(i), arity=i, notation='CONDENSED'))

    for char in ['p', 'q', 'r', 's']:
        for i in range(max_args + 1):
            signature.add_symbol(PredicateSymbol(char + itoa_superscripts(i), arity=i))

    return signature
