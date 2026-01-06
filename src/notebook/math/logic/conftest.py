import pytest

from ...support.unicode import itoa_superscripts
from .signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol, SignatureSymbolNotation


@pytest.fixture
def dummy_signature(max_args: int = 3) -> FormalLogicSignature:
    signature = FormalLogicSignature(
        FunctionSymbol('∘', arity=2, notation=SignatureSymbolNotation.INFIX),
        PredicateSymbol('≠', arity=2, notation=SignatureSymbolNotation.INFIX),
    )

    for char in ['f', 'g', 'h', 't']:
        signature.add_symbol(FunctionSymbol(char + 'ᶜ⁰', arity=0))

        for i in range(1, max_args + 1):
            signature.add_symbol(FunctionSymbol(char + itoa_superscripts(i), arity=i, notation=SignatureSymbolNotation.PREFIX))
            signature.add_symbol(FunctionSymbol(char + 'ᶜ' + itoa_superscripts(i), arity=i, notation=SignatureSymbolNotation.CONDENSED))

    for char in ['p', 'q', 'r', 's']:
        signature.add_symbol(PredicateSymbol(char + 'ᶜ⁰', arity=0))

        for i in range(1, max_args + 1):
            signature.add_symbol(PredicateSymbol(char + itoa_superscripts(i), arity=i, notation=SignatureSymbolNotation.PREFIX))

    return signature
