import pytest

from ..logic.signature import FormalLogicSignature
from .signature import LambdaSignature
from .type_system.explicit import SIMPLE_SIGNATURE


@pytest.fixture
def dummy_signature() -> LambdaSignature:
    return LambdaSignature(base_types=['τ', 'σ', 'ρ'])
