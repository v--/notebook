import pytest

from ...logic.propositional import PROPOSITIONAL_SIGNATURE, PropositionalLogicSignature
from ...logic.signature import FormalLogicSignature
from ..algebraic_types import SIMPLE_ALGEBRAIC_SIGNATURE
from ..signature import LambdaSignature


@pytest.fixture
def ch_logic_dummy_signature() -> FormalLogicSignature:
    return PropositionalLogicSignature(['τ', 'σ', 'ρ'])
