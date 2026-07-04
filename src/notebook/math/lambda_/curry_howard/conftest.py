import pytest

from notebook.math.logic.propositional import PropLogicSignature, PropVariableSymbol
lazy from notebook.math.logic.signature import FormalLogicSignature


@pytest.fixture
def ch_logic_dummy_signature() -> FormalLogicSignature:
    return PropLogicSignature(
        *(PropVariableSymbol(chr(i)) for i in range(ord('α'), ord('ω') + 1)),
    )
