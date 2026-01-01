import pytest

from ...logic.propositional import PropLogicSignature, PropVariableSymbol
from ...logic.signature import FormalLogicSignature


@pytest.fixture
def ch_logic_dummy_signature() -> FormalLogicSignature:
    return PropLogicSignature(
        *(PropVariableSymbol(chr(i)) for i in range(ord('α'), ord('ω') + 1))
    )
