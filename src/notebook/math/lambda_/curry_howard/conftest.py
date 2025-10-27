import pytest

from ...logic.signature import FormalLogicSignature
from ..algebraic_types import SIMPLE_ALGEBRAIC_SIGNATURE
from ..signature import LambdaSignature


@pytest.fixture
def ch_logic_dummy_signature() -> FormalLogicSignature:
    signature = FormalLogicSignature()
    signature.add_symbol('PREDICATE', name='τ', arity=0)
    signature.add_symbol('PREDICATE', name='σ', arity=0)
    signature.add_symbol('PREDICATE', name='ρ', arity=0)
    return signature
