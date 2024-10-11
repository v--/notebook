from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from ..fol.formulas import ConnectiveFormula, ConstantFormula, Formula, NegationFormula, QuantifierFormula
from .exceptions import NaturalDeductionError
from .parsing.parser import parse_placeholder, parse_schema
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


@dataclass(frozen=True)
class Substitution:
    mapping: Mapping[FormulaPlaceholder, Formula]

    def __or__(self, other: object) -> 'Substitution | None':
        if not isinstance(other, Substitution):
            return NotImplemented

        a = self.mapping
        b = other.mapping
        common_keys = set(set(a.keys()) & set(b.keys()))

        if all(a[pl] == b[pl] for pl in common_keys):
            return Substitution({**a, **b})

        return None


EMPTY_SUBSTITUTION = Substitution({})


@dataclass(frozen=True)
class SubstitutionApplicationVisitor(FormulaSchemaVisitor[Formula]):
    substitution: Substitution

    @override
    def visit_constant(self, schema: ConstantFormulaSchema) -> ConstantFormula:
        return ConstantFormula(schema.value)

    @override
    def visit_atomic(self, schema: FormulaPlaceholder) -> Formula:
        if schema not in self.substitution.mapping:
            raise SubstitutionError(f'No specification of how to substitute {schema}')

        return self.substitution.mapping[schema]

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


def apply_substitution(schema: FormulaSchema, substitution: Substitution) -> Formula:
    return SubstitutionApplicationVisitor(substitution).visit(schema)


def substitute(schema: str, **kwargs: Formula) -> Formula:
    substitution = Substitution({ parse_placeholder(key): value for key, value in kwargs.items() })
    return apply_substitution(parse_schema(schema), substitution)


@dataclass(frozen=True)
class BuildSubstitutionVisitor(FormulaSchemaVisitor[Substitution | None]):
    formula: Formula

    @override
    def visit_constant(self, schema: ConstantFormulaSchema) -> Substitution | None:
        if isinstance(self.formula, ConstantFormula) and self.formula.value == schema.value:
            return Substitution({})

        return None

    @override
    def visit_atomic(self, schema: FormulaPlaceholder) -> Substitution:
        return Substitution({schema: self.formula})

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> Substitution | None:
        if isinstance(self.formula, NegationFormula):
            return BuildSubstitutionVisitor(self.formula.sub).visit(schema.sub)

        return None

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> Substitution | None:
        if isinstance(self.formula, ConnectiveFormula) and self.formula.conn == schema.conn:
            a = BuildSubstitutionVisitor(self.formula.a).visit(schema.a)
            b = BuildSubstitutionVisitor(self.formula.b).visit(schema.b)

            if a is None or b is None:
                return None

            return a | b

        return None

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> Substitution | None:
        if isinstance(self.formula, QuantifierFormula) and self.formula.quantifier == schema.quantifier:
            return BuildSubstitutionVisitor(self.formula.sub).visit(schema.sub)

        return None


def build_substitution(schema: FormulaSchema, formula: Formula) -> Substitution | None:
    return BuildSubstitutionVisitor(formula).visit(schema)


def is_schema_instance(schema: FormulaSchema, formula: Formula) -> bool:
    return build_substitution(schema, formula) is not None
