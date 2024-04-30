from dataclasses import dataclass
from typing import override

from ..fol.formulas import ConnectiveFormula, ConstantFormula, Formula, NegationFormula, QuantifierFormula
from .exceptions import NaturalDeductionError
from .schemas import (
    ConnectiveFormulaSchema,
    ConstantFormulaSchema,
    FormulaPlaceholder,
    FormulaSchema,
    NegationFormulaSchema,
    QuantifierFormulaSchema,
)
from .visitors import FormulaSchemaVisitor


class SubstitutionError(NaturalDeductionError):
    pass


@dataclass
class UniformSubstitutionApplicationVisitor(FormulaSchemaVisitor[Formula]):
    atomic_mapping: dict[FormulaPlaceholder, Formula]

    @override
    def visit_constant(self, schema: ConstantFormulaSchema) -> ConstantFormula:
        return ConstantFormula(schema.value)

    @override
    def visit_atomic(self, schema: FormulaPlaceholder) -> Formula:
        if schema not in self.atomic_mapping:
            raise SubstitutionError(f'No specification how to substitute {schema}')

        return self.atomic_mapping[schema]

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> NegationFormula:
        return NegationFormula(self.visit(schema.sub))

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> ConnectiveFormula:
        return ConnectiveFormula(
            schema.conn,
            self.visit(schema.a),
            self.visit(schema.b)
        )

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> QuantifierFormula:
        return QuantifierFormula(
            schema.quantifier,
            schema.variable,
            self.visit(schema.sub)
        )


@dataclass
class UniformSubstitution:
    atomic_mapping: dict[FormulaPlaceholder, Formula]

    def apply_to(self, schema: FormulaSchema) -> Formula:
        return UniformSubstitutionApplicationVisitor(self.atomic_mapping).visit(schema)

    def __and__(self, other: object) -> 'UniformSubstitution | None':
        if not isinstance(other, UniformSubstitution):
            return NotImplemented

        a = self.atomic_mapping
        b = other.atomic_mapping
        common_keys = set(set(a.keys()) & set(b.keys()))

        if all(a[pl] == b[pl] for pl in common_keys):
            return UniformSubstitution({**a, **b})

        return None


EMPTY_SUBSTITUTION = UniformSubstitution({})


@dataclass
class BuildUniformSubstitutionVisitor(FormulaSchemaVisitor[UniformSubstitution | None]):
    formula: Formula

    @override
    def visit_constant(self, schema: ConstantFormulaSchema) -> UniformSubstitution | None:
        if isinstance(self.formula, ConstantFormula) and self.formula.value == schema.value:
            return UniformSubstitution({})

        return None

    @override
    def visit_atomic(self, schema: FormulaPlaceholder) -> UniformSubstitution:
        return UniformSubstitution({schema: self.formula})

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> UniformSubstitution | None:
        if isinstance(self.formula, NegationFormula):
            return BuildUniformSubstitutionVisitor(self.formula.sub).visit(schema.sub)

        return None

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> UniformSubstitution | None:
        if isinstance(self.formula, ConnectiveFormula) and self.formula.conn == schema.conn:
            a = BuildUniformSubstitutionVisitor(self.formula.a).visit(schema.a)
            b = BuildUniformSubstitutionVisitor(self.formula.b).visit(schema.b)

            if a is None or b is None:
                return None

            return a & b

        return None

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> UniformSubstitution | None:
        if isinstance(self.formula, QuantifierFormula) and self.formula.quantifier == schema.quantifier:
            return BuildUniformSubstitutionVisitor(self.formula.sub).visit(schema.sub)

        return None


def build_substitution(schema: FormulaSchema, formula: Formula) -> UniformSubstitution | None:
    return BuildUniformSubstitutionVisitor(formula).visit(schema)


def is_schema_instance(schema: FormulaSchema, formula: Formula) -> bool:
    return build_substitution(schema, formula) is not None
