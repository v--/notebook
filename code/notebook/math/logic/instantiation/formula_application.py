from typing import override

from ....support.schemas import SchemaInstantiationError
from ..formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
    ConstantFormula,
    EqualityFormula,
    EqualityFormulaSchema,
    Formula,
    FormulaPlaceholder,
    FormulaSchema,
    FormulaSchemaVisitor,
    NegationFormula,
    NegationFormulaSchema,
    PredicateFormula,
    PredicateFormulaSchema,
    QuantifierFormula,
    QuantifierFormulaSchema,
)
from .base import FormalLogicSchemaInstantiation
from .term_application import InstantiationApplicationVisitor as TermInstantiationApplicationVisitor


class InstantiationApplicationVisitor(FormulaSchemaVisitor[Formula]):
    instantiation: FormalLogicSchemaInstantiation
    term_visitor: TermInstantiationApplicationVisitor

    def __init__(self, instantiation: FormalLogicSchemaInstantiation) -> None:
        self.instantiation = instantiation
        self.term_visitor = TermInstantiationApplicationVisitor(self.instantiation)

    @override
    def visit_constant(self, schema: ConstantFormula) -> ConstantFormula:
        return ConstantFormula(schema.value)

    @override
    def visit_equality(self, schema: EqualityFormulaSchema) -> EqualityFormula:
        return EqualityFormula(self.term_visitor.visit(schema.left), self.term_visitor.visit(schema.right))

    @override
    def visit_predicate(self, schema: PredicateFormulaSchema) -> PredicateFormula:
        return PredicateFormula(schema.name, [self.term_visitor.visit(arg) for arg in schema.arguments])

    @override
    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> Formula:
        if schema not in self.instantiation.formula_mapping:
            raise SchemaInstantiationError(f'No specification of how to instantiate the formula placeholder {schema}')

        return self.instantiation.formula_mapping[schema]

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> NegationFormula:
        return NegationFormula(self.visit(schema.body))

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> ConnectiveFormula:
        return ConnectiveFormula(
            schema.conn,
            self.visit(schema.left),
            self.visit(schema.right)
        )

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> QuantifierFormula:
        return QuantifierFormula(
            schema.quantifier,
            self.term_visitor.visit_variable_placeholder(schema.var),
            self.visit(schema.body)
        )


def instantiate_formula_schema(schema: FormulaSchema, instantiation: FormalLogicSchemaInstantiation) -> Formula:
    return InstantiationApplicationVisitor(instantiation).visit(schema)
