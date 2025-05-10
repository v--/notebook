import pytest

from ...logic.signature import FormalLogicSignature
from ..signature import LambdaSignature
from ..type_system.explicit import SIMPLE_SIGNATURE


@pytest.fixture
def ch_logic_dummy_signature() -> FormalLogicSignature:
    signature = FormalLogicSignature()
    signature.add_symbol('PREDICATE', name='τ', arity=0)
    signature.add_symbol('PREDICATE', name='σ', arity=0)
    signature.add_symbol('PREDICATE', name='ρ', arity=0)
    return signature


@pytest.fixture
def ch_lambda_dummy_signature() -> LambdaSignature:
    signature = LambdaSignature(base_types=['τ', 'σ', 'ρ'])

    for sym in SIMPLE_SIGNATURE.iter_symbols():
        signature.add_symbol(sym.kind, sym.name)

    return signature
