from collections.abc import Iterator, Mapping
from dataclasses import dataclass

from ..deduction import NaturalDeductionRule, NaturalDeductionSystem
from ..formulas import ExtendedFormulaSchema, Formula
from ..instantiation import is_formula_schema_instance
from ..parsing import parse_signatureless_natural_deduction_rule


MODUS_PONENS_RULE = parse_signatureless_natural_deduction_rule('(φ → ψ), φ ⫢ ψ')


@dataclass(frozen=True)
class AxiomaticDerivationSystem(Mapping[str, ExtendedFormulaSchema]):
    axiom_schemas: Mapping[str, ExtendedFormulaSchema]

    def is_axiom(self, formula: Formula) -> bool:
        return any(is_formula_schema_instance(schema, formula) for schema in self.axiom_schemas.values())

    def __getitem__(self, key: str) -> ExtendedFormulaSchema:
        return self.axiom_schemas[key]

    def __contains__(self, key: object) -> bool:
        return key in self.axiom_schemas

    def __len__(self) -> int:
        return len(self.axiom_schemas)

    def __iter__(self) -> Iterator[str]:
        return iter(self.axiom_schemas)


def derivation_system_to_natural_deduction_system(system: AxiomaticDerivationSystem) -> NaturalDeductionSystem:
    return NaturalDeductionSystem({
        'MP': MODUS_PONENS_RULE
    } | {
        name: NaturalDeductionRule(premises=[], conclusion=schema)
        for name, schema in system.axiom_schemas.items()
    })
