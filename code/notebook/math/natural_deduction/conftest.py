from collections.abc import Sequence

import pytest

from ..fol.parsing import parse_propositional_formula
from .minimal_implicational_logic import get_identity_derivation_payload


IDENTITY_DERIVATION = [
    str(f) for f in
    get_identity_derivation_payload(parse_propositional_formula('p'))
]


@pytest.fixture
def identity_derivation() -> Sequence[str]:
    return IDENTITY_DERIVATION
