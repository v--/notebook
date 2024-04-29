import pytest

from ..fol.conftest import dummy_signature, propositional_signature
from .parsing.parser import parse_placeholder
from .rules import FormulaPlaceholder


@pytest.fixture()
def implicational_axioms() -> frozenset[FormulaPlaceholder]:
    return frozenset([
        parse_placeholder('(Φ → (Ψ → Φ))'),
        parse_placeholder('((Φ → (Ψ → Θ)) → ((Φ → Ψ) → (Φ → Θ)))'),
    ])
