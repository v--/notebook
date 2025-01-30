from typing import override

from ....support.schemas import SchemaInstantiationError
from ..formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
    ConstantFormula,
    EqualityFormula,
    EqualityFormulaSchema,
    ExtendedFormulaSchema,
    Formula,
    FormulaPlaceholder,
    FormulaSchemaVisitor,
    NegationFormula,
    NegationFormulaSchema,
    PredicateFormula,
    PredicateFormulaSchema,
    QuantifierFormula,
    QuantifierFormulaSchema,
    SubstitutionSchema,
)
from ..substitution import substitute_in_formula
from ..terms import Variable
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
        return EqualityFormula(self.term_visitor.visit(schema.a), self.term_visitor.visit(schema.b))

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

    @override
    def visit_substitution(self, schema: SubstitutionSchema) -> Formula:
        formula = self.visit(schema.formula)
        var = self.term_visitor.visit_variable_placeholder(schema.var)
        dest = self.term_visitor.visit(schema.dest)
        return substitute_in_formula(formula, var, dest)


def instantiate_formula_schema(schema: ExtendedFormulaSchema, instantiation: FormalLogicSchemaInstantiation) -> Formula:
    return InstantiationApplicationVisitor(instantiation).visit(schema)
