from typing import TYPE_CHECKING

import pytest

from notebook.math.logic.propositional import PropLogicSignature, PropVariableSymbol


if TYPE_CHECKING:
    from notebook.math.logic.signature import FormalLogicSignature


@pytest.fixture
def ch_logic_dummy_signature() -> FormalLogicSignature:
    return PropLogicSignature(
        *(PropVariableSymbol(chr(i)) for i in range(ord('α'), ord('ω') + 1)),
    )
