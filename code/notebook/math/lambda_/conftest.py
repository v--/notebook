import pytest

from .signature import LambdaSignature


@pytest.fixture
def dummy_signature() -> LambdaSignature:
    return LambdaSignature(base_types={'τ', 'σ', 'ρ'}, constant_terms=set())
