import pytest

from ...logic.propositional import PropositionalLogicSignature, PropositionalVariable
from ...logic.signature import FormalLogicSignature


@pytest.fixture
def ch_logic_dummy_signature() -> FormalLogicSignature:
    return PropositionalLogicSignature(
        *(PropositionalVariable(chr(i)) for i in range(ord('α'), ord('ω') + 1))
    )
