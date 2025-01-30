from collections.abc import Collection
from typing import NamedTuple

from ..deduction.rules import NaturalDeductionRule, NaturalDeductionSystem
from ..formulas import ExtendedFormulaSchema, Formula
from ..instantiation import is_formula_schema_instance
from ..parsing import parse_signatureless_natural_deduction_rule


MODUS_PONENS_RULE = parse_signatureless_natural_deduction_rule('(MP) (φ → ψ), φ ⫢ ψ')


class AxiomaticDerivationSystem(NamedTuple):
    axiom_schemas: Collection[ExtendedFormulaSchema]


def is_axiom(system: AxiomaticDerivationSystem, formula: Formula) -> bool:
    return any(is_formula_schema_instance(schema, formula) for schema in system.axiom_schemas)


def derivation_system_to_natural_deduction_system(system: AxiomaticDerivationSystem) -> NaturalDeductionSystem:
    return NaturalDeductionSystem(
        rules=[
            MODUS_PONENS_RULE
        ] + [
            NaturalDeductionRule(name='Ax', premises=[], conclusion=axiom_schema)
            for axiom_schema in system.axiom_schemas
        ]
    )
