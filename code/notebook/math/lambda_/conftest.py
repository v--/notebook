import pytest

from .signature import LambdaSignature


@pytest.fixture
def dummy_signature() -> LambdaSignature:
    return LambdaSignature(base_types={'α', 'β', 'γ'}, constant_terms=set())
