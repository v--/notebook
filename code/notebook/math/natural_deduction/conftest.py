import pytest

from ..fol.conftest import dummy_signature, propositional_signature
from .parsing.parser import parse_schema
from .rules import FormulaSchema


@pytest.fixture()
def implicational_axioms() -> frozenset[FormulaSchema]:
    return frozenset([
        parse_schema('(Φ → (Ψ → Φ))'),
        parse_schema('((Φ → (Ψ → Θ)) → ((Φ → Ψ) → (Φ → Θ)))'),
    ])
