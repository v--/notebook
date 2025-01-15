from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from .exceptions import FOLError
from .formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
    ConstantFormula,
    ExtendedFormulaSchema,
    Formula,
    FormulaPlaceholder,
    NegationFormula,
    NegationFormulaSchema,
    QuantifierFormula,
    QuantifierFormulaSchema,
)
from .terms import Variable
from .visitors import FormulaSchemaVisitor


class SchemaInstantiationError(FOLError):
    pass


@dataclass(frozen=True)
class SchemaInstantiation:
    mapping: Mapping[FormulaPlaceholder, Formula]

    def __or__(self, other: object) -> 'SchemaInstantiation | None':
        if not isinstance(other, SchemaInstantiation):
            return NotImplemented

        a = self.mapping
        b = other.mapping
        common_keys = set(set(a.keys()) & set(b.keys()))

        if all(a[pl] == b[pl] for pl in common_keys):
            return SchemaInstantiation({**a, **b})

        return None


EMPTY_SUBSTITUTION = SchemaInstantiation({})


@dataclass(frozen=True)
class InstantiationVisitor(FormulaSchemaVisitor[Formula]):
    instantiation: SchemaInstantiation

    @override
    def visit_constant(self, schema: ConstantFormula) -> ConstantFormula:
        return ConstantFormula(schema.value)

    @override
    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> Formula:
        if schema not in self.instantiation.mapping:
            raise SchemaInstantiationError(f'No specification of how to interpret {schema}')

        return self.instantiation.mapping[schema]

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
            Variable(schema.variable.identifier),
            self.visit(schema.sub)
        )


def instantiate_schema(schema: ExtendedFormulaSchema, instantiation: SchemaInstantiation) -> Formula:
    return InstantiationVisitor(instantiation).visit(schema)


@dataclass(frozen=True)
class BuildInterpretationVisitor(FormulaSchemaVisitor[SchemaInstantiation | None]):
    formula: Formula

    @override
    def visit_constant(self, schema: ConstantFormula) -> SchemaInstantiation | None:
        if isinstance(self.formula, ConstantFormula) and self.formula.value == schema.value:
            return SchemaInstantiation({})

        return None

    @override
    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> SchemaInstantiation:
        return SchemaInstantiation({schema: self.formula})

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> SchemaInstantiation | None:
        if isinstance(self.formula, NegationFormula):
            return BuildInterpretationVisitor(self.formula.sub).visit(schema.sub)

        return None

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> SchemaInstantiation | None:
        if isinstance(self.formula, ConnectiveFormula) and self.formula.conn == schema.conn:
            a = BuildInterpretationVisitor(self.formula.a).visit(schema.a)
            b = BuildInterpretationVisitor(self.formula.b).visit(schema.b)

            if a is None or b is None:
                return None

            return a | b

        return None

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> SchemaInstantiation | None:
        if isinstance(self.formula, QuantifierFormula) and self.formula.quantifier == schema.quantifier:
            return BuildInterpretationVisitor(self.formula.sub).visit(schema.sub)

        return None


def build_instantiation(schema: ExtendedFormulaSchema, formula: Formula) -> SchemaInstantiation | None:
    return BuildInterpretationVisitor(formula).visit(schema)


def is_schema_instance(schema: ExtendedFormulaSchema, formula: Formula) -> bool:
    return build_instantiation(schema, formula) is not None
