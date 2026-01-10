from ..contexts import LogicalContext
from ..parsing import parse_context_placeholder, parse_formula_placeholder, parse_sequent_schema
from ..propositional import parse_prop_formula
from ..sequents import Sequent
from .base import AtomicLogicSchemaInstantiation
from .sequent_application import instantiate_sequent_schema


def test_instantiate_context_schema() -> None:
    schema = parse_sequent_schema('(Γ, φ ⊢ ψ, Δ)')
    instantiation = AtomicLogicSchemaInstantiation(
        formula_mapping={
            parse_formula_placeholder('φ'): parse_prop_formula('q'),
            parse_formula_placeholder('ψ'): parse_prop_formula('r')
        },
        context_mapping={
            parse_context_placeholder('Γ'): [parse_prop_formula('p')],
            parse_context_placeholder('Δ'): []
        }
    )

    expected = Sequent(
        LogicalContext([parse_prop_formula('p'), parse_prop_formula('q')]),
        LogicalContext([parse_prop_formula('r')])
    )

    assert instantiate_sequent_schema(schema, instantiation) == expected
