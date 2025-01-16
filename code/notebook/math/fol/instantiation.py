from collections.abc import Mapping
from dataclasses import dataclass
from typing import override

from .exceptions import FOLError
from .formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
    ConstantFormula,
    EqualityFormula,
    EqualityFormulaSchema,
    ExtendedFormulaSchema,
    Formula,
    FormulaPlaceholder,
    NegationFormula,
    NegationFormulaSchema,
    PredicateFormula,
    PredicateFormulaSchema,
    QuantifierFormula,
    QuantifierFormulaSchema,
    SubstitutionSchema,
)
from .substitution import substitute_in_formula
from .terms import FunctionTerm, FunctionTermSchema, Term, TermPlaceholder, Variable, VariablePlaceholder
from .visitors import FormulaSchemaVisitor, TermSchemaVisitor


class SchemaInstantiationError(FOLError):
    pass


def coincide_on_common_keys[T, S](a: Mapping[T, S], b: Mapping[T, S]) -> bool:
    common_keys = set(set(a.keys()) & set(b.keys()))
    return all(a[pl] == b[pl] for pl in common_keys)


class SchemaInstantiation:
    formula_mapping: Mapping[FormulaPlaceholder, Formula]
    variable_mapping: Mapping[VariablePlaceholder, Variable]
    term_mapping: Mapping[TermPlaceholder, Term]

    def __init__(
        self,
        *,
        formula_mapping: Mapping[FormulaPlaceholder, Formula] | None = None,
        variable_mapping: Mapping[VariablePlaceholder, Variable] | None = None,
        term_mapping: Mapping[TermPlaceholder, Term] | None = None
    ) -> None:
        self.formula_mapping = formula_mapping or {}
        self.variable_mapping = variable_mapping or {}
        self.term_mapping = term_mapping or {}

    def is_instantiation_compatible(self, other: 'SchemaInstantiation') -> bool:
        return coincide_on_common_keys(self.formula_mapping, other.formula_mapping) and \
            coincide_on_common_keys(self.variable_mapping, other.variable_mapping) and \
            coincide_on_common_keys(self.term_mapping, other.term_mapping)

    def __or__(self, other: object) -> 'SchemaInstantiation | None':
        if not isinstance(other, SchemaInstantiation):
            return NotImplemented

        if not self.is_instantiation_compatible(other):
            return None

        return SchemaInstantiation(
            formula_mapping={**self.formula_mapping, **other.formula_mapping},
            variable_mapping={**self.variable_mapping, **other.variable_mapping},
            term_mapping={**self.term_mapping, **other.term_mapping}
        )


EMPTY_SUBSTITUTION = SchemaInstantiation()


class TermInstantiationVisitor(TermSchemaVisitor[Term]):
    instantiation: SchemaInstantiation

    def __init__(self, instantiation: SchemaInstantiation) -> None:
        self.instantiation = instantiation

    @override
    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> Variable:
        if schema not in self.instantiation.variable_mapping:
            raise SchemaInstantiationError(f'No specification of how to instantiate the variable placeholder {schema}')

        return self.instantiation.variable_mapping[schema]

    @override
    def visit_term_placeholder(self, schema: TermPlaceholder) -> Term:
        if schema not in self.instantiation.term_mapping:
            raise SchemaInstantiationError(f'No specification of how to instantiate the term placeholder {schema}')

        return self.instantiation.term_mapping[schema]

    @override
    def visit_function(self, schema: FunctionTermSchema) -> FunctionTerm:
        return FunctionTerm(schema.name, [self.visit(arg) for arg in schema.arguments])


class InstantiationVisitor(FormulaSchemaVisitor[Formula]):
    instantiation: SchemaInstantiation
    term_visitor: TermInstantiationVisitor

    def __init__(self, instantiation: SchemaInstantiation) -> None:
        self.instantiation = instantiation
        self.term_visitor = TermInstantiationVisitor(instantiation)

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


def instantiate_schema(schema: ExtendedFormulaSchema, instantiation: SchemaInstantiation) -> Formula:
    return InstantiationVisitor(instantiation).visit(schema)


@dataclass(frozen=True)
class BuildInterpretationVisitor(FormulaSchemaVisitor[SchemaInstantiation | None]):
    formula: Formula

    @override
    def visit_constant(self, schema: ConstantFormula) -> SchemaInstantiation | None:
        if isinstance(self.formula, ConstantFormula) and self.formula.value == schema.value:
            return SchemaInstantiation()

        return None

    @override
    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> SchemaInstantiation:
        return SchemaInstantiation(formula_mapping={schema: self.formula})

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
