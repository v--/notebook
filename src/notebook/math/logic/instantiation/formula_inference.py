from dataclasses import dataclass
from typing import override

from ....support.schemas import SchemaInferenceError
from ..formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
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
    PropConstant,
    QuantifierFormula,
    QuantifierFormulaSchema,
)
from .base import AtomicLogicSchemaInstantiation
from .term_inference import infer_instantiation_from_term


@dataclass(frozen=True)
class InferInstantiationVisitor(FormulaSchemaVisitor[AtomicLogicSchemaInstantiation]):
    formula: Formula

    @override
    def visit_prop_constant(self, schema: PropConstant) -> AtomicLogicSchemaInstantiation:
        if self.formula != schema:
            raise SchemaInferenceError(f'Cannot match constant {schema} to {self.formula}')

        return AtomicLogicSchemaInstantiation()

    @override
    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> AtomicLogicSchemaInstantiation:
        return AtomicLogicSchemaInstantiation(formula_mapping={schema: self.formula})

    @override
    def visit_equality(self, schema: EqualityFormulaSchema) -> AtomicLogicSchemaInstantiation:
        if not isinstance(self.formula, EqualityFormula):
            raise SchemaInferenceError(f'Cannot match negation schema {schema} to {self.formula}')

        left = infer_instantiation_from_term(schema.left, self.formula.left)
        right = infer_instantiation_from_term(schema.right, self.formula.right)

        return left | right

    @override
    def visit_predicate(self, schema: PredicateApplicationSchema) -> AtomicLogicSchemaInstantiation:
        if not isinstance(self.formula, PredicateApplication) or schema.symbol != self.formula.symbol or len(schema.arguments) != len(self.formula.arguments):
            raise SchemaInferenceError(f'Cannot match predicate formula schema {schema} to {self.formula}')

        instantiation = AtomicLogicSchemaInstantiation()

        for subschema, subterm in zip(schema.arguments, self.formula.arguments, strict=True):
            instantiation |= infer_instantiation_from_term(subschema, subterm)

        return instantiation

    @override
    def visit_negation(self, schema: NegationFormulaSchema) -> AtomicLogicSchemaInstantiation:
        if not isinstance(self.formula, NegationFormula):
            raise SchemaInferenceError(f'Cannot match negation schema {schema} to {self.formula}')

        return infer_instantiation_from_formula(schema.body, self.formula.body)

    @override
    def visit_connective(self, schema: ConnectiveFormulaSchema) -> AtomicLogicSchemaInstantiation:
        if not isinstance(self.formula, ConnectiveFormula) or self.formula.conn != schema.conn:
            raise SchemaInferenceError(f'Cannot match connective formula schema {schema} to {self.formula}')

        left = infer_instantiation_from_formula(schema.left, self.formula.left)
        right = infer_instantiation_from_formula(schema.right, self.formula.right)

        return left | right

    @override
    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> AtomicLogicSchemaInstantiation:
        if not isinstance(self.formula, QuantifierFormula) or self.formula.quant != schema.quant:
            raise SchemaInferenceError(f'Cannot match quantifier formula schema {schema} to {self.formula}')

        var = infer_instantiation_from_term(schema.var, self.formula.var)
        body = infer_instantiation_from_formula(schema.body, self.formula.body)

        return var | body


def infer_instantiation_from_formula(schema: FormulaSchema, formula: Formula) -> AtomicLogicSchemaInstantiation:
    return InferInstantiationVisitor(formula).visit(schema)


def is_formula_schema_instance(schema: FormulaSchema, formula: Formula) -> bool:
    try:
        infer_instantiation_from_formula(schema, formula)
    except SchemaInferenceError:
        return False
    else:
        return True
