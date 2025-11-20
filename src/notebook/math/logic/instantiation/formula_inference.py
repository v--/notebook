from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInferenceError
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
    PredicateApplication,
    PredicateApplicationSchema,
    QuantifierFormula,
    QuantifierFormulaSchema,
)
from .base import FormalLogicSchemaInstantiation
from .term_inference import infer_instantiation_from_term


@dataclass(frozen=True)
class InferInstantiationVisitor(FormulaSchemaVisitor[FormalLogicSchemaInstantiation]):
    formula: Formula

    @override
    def visit_logical_constant(self, schema: ConstantFormula) -> FormalLogicSchemaInstantiation:
        if self.formula != schema:
            raise SchemaInferenceError(f'Cannot match constant {schema} to {self.formula}')

        return FormalLogicSchemaInstantiation()

    @override
    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> FormalLogicSchemaInstantiation:
        return FormalLogicSchemaInstantiation(formula_mapping={schema: self.formula})

    @override
    def visit_equality(self, schema: EqualityFormulaSchema) -> FormalLogicSchemaInstantiation:
        if not isinstance(self.formula, EqualityFormula):
            raise SchemaInferenceError(f'Cannot match negation schema {schema} to {self.formula}')

        left = infer_instantiation_from_term(schema.left, self.formula.left)
        right = infer_instantiation_from_term(schema.right, self.formula.right)

        return left | right

    @override
    def visit_predicate(self, schema: PredicateApplicationSchema) -> FormalLogicSchemaInstantiation:
        if not isinstance(self.formula, PredicateApplication) or schema.name != self.formula.name or len(schema.arguments) != len(self.formula.arguments):
            raise SchemaInferenceError(f'Cannot match predicate formula schema {schema} to {self.formula}')

        instantiation = FormalLogicSchemaInstantiation()

        for subschema, subterm in zip(schema.arguments, self.formula.arguments, strict=True):
            instantiation |= infer_instantiation_from_term(subschema, subterm)

        return instantiation

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> FormalLogicSchemaInstantiation:
        if not isinstance(self.formula, NegationFormula):
            raise SchemaInferenceError(f'Cannot match negation schema {schema} to {self.formula}')

        return infer_instantiation_from_formula(schema.body, self.formula.body)

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> FormalLogicSchemaInstantiation:
        if not isinstance(self.formula, ConnectiveFormula) or self.formula.conn != schema.conn:
            raise SchemaInferenceError(f'Cannot match connective formula schema {schema} to {self.formula}')

        left = infer_instantiation_from_formula(schema.left, self.formula.left)
        right = infer_instantiation_from_formula(schema.right, self.formula.right)

        return left | right

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> FormalLogicSchemaInstantiation:
        if not isinstance(self.formula, QuantifierFormula) or self.formula.quantifier != schema.quantifier:
            raise SchemaInferenceError(f'Cannot match quantifier formula schema {schema} to {self.formula}')

        var = infer_instantiation_from_term(schema.var, self.formula.var)
        body = infer_instantiation_from_formula(schema.body, self.formula.body)

        return var | body


def infer_instantiation_from_formula(schema: FormulaSchema, formula: Formula) -> FormalLogicSchemaInstantiation:
    return InferInstantiationVisitor(formula).visit(schema)


def is_formula_schema_instance(schema: FormulaSchema, formula: Formula) -> bool:
    try:
        infer_instantiation_from_formula(schema, formula)
    except SchemaInferenceError:
        return False
    else:
        return True
