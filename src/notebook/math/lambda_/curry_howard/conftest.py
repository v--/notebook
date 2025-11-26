import pytest

from ...logic.propositional import PropositionalLogicSignature, PropositionalVariable
from ...logic.signature import FormalLogicSignature


@pytest.fixture
def ch_logic_dummy_signature() -> FormalLogicSignature:
    signature = PropositionalLogicSignature()

    for ind in range(ord('α'), ord('ω') + 1):
        signature.add_symbol(PropositionalVariable(chr(ind)))

    return signature
