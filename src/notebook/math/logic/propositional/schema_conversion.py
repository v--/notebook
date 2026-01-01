from typing import override

from ..formulas import (
    ConnectiveFormulaSchema,
    EqualityFormulaSchema,
    FormulaPlaceholder,
    FormulaSchema,
    FormulaSchemaVisitor,
    NegationFormulaSchema,
    PredicateApplicationSchema,
    PropConstant,
    QuantifierFormulaSchema,
)
from .exceptions import NonPropositionalFormulaError
from .schemas import PropConnectiveFormulaSchema, PropFormulaSchema, PropNegationFormulaSchema, PropPlaceholder


class PropFormulaSchemaConversionVisitor(FormulaSchemaVisitor[PropFormulaSchema]):
    @override
    def visit_prop_constant(self, schema: PropConstant) -> PropConstant:
        return schema

    @override
    def visit_equality(self, schema: EqualityFormulaSchema) -> PropFormulaSchema:
        raise NonPropositionalFormulaError(f'Unexpected equality {schema} in propositional schema')

    @override
    def visit_predicate(self, schema: PredicateApplicationSchema) -> PropFormulaSchema:
        raise NonPropositionalFormulaError(f'Unexpected predicate symbol {schema} in propositional schema')

    @override
    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> PropPlaceholder:
        return PropPlaceholder(schema.identifier)

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> PropNegationFormulaSchema:
        return PropNegationFormulaSchema(self.visit(schema.body))

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> PropConnectiveFormulaSchema:
        return PropConnectiveFormulaSchema(
            schema.conn,
            self.visit(schema.left),
            self.visit(schema.right)
        )

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> PropFormulaSchema:
        raise NonPropositionalFormulaError(f'Unexpected quantifier {schema.quant} in propositional schema')


def convert_to_prop_schema(schema: FormulaSchema) -> PropFormulaSchema:
    return PropFormulaSchemaConversionVisitor().visit(schema)
