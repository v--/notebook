from .formulas import (
    ConnectiveFormula,
    ConnectiveFormulaSchema,
    ConstantFormula,
    EqualityFormula,
    EqualityFormulaSchema,
    ExtendedFormulaSchema,
    Formula,
    FormulaPlaceholder,
    FormulaSchema,
    NegationFormula,
    NegationFormulaSchema,
    PredicateFormula,
    QuantifierFormula,
    QuantifierFormulaSchema,
    SubstitutionSchema,
)
from .terms import FunctionTerm, FunctionTermSchema, Term, TermPlaceholder, TermSchema, Variable, VariablePlaceholder


class TermVisitor[T]:
    def visit(self, term: Term) -> T:
        match term:
            case Variable():
                return self.visit_variable(term)

            case FunctionTerm():
                return self.visit_function(term)

    def visit_variable(self, term: Variable) -> T:
        return self.generic_visit(term)

    def visit_function(self, term: FunctionTerm) -> T:
        return self.generic_visit(term)

    def generic_visit(self, term: Term) -> T:
        raise NotImplementedError


class TermTransformationVisitor(TermVisitor[Term]):
    def visit_variable(self, term: Variable) -> Term:
        return term

    def visit_function(self, term: FunctionTerm) -> Term:
        return FunctionTerm(
            term.name,
            [self.visit(arg) for arg in term.arguments]
        )


class FormulaVisitor[T]:
    def visit(self, formula: Formula) -> T:
        match formula:
            case ConstantFormula():
                return self.visit_constant(formula)

            case EqualityFormula():
                return self.visit_equality(formula)

            case PredicateFormula():
                return self.visit_predicate(formula)

            case NegationFormula():
                return self.visit_negation(formula)

            case ConnectiveFormula():
                return self.visit_connective(formula)

            case QuantifierFormula():
                return self.visit_quantifier(formula)

    def visit_constant(self, formula: ConstantFormula) -> T:
        return self.generic_visit(formula)

    def visit_equality(self, formula: EqualityFormula) -> T:
        return self.generic_visit(formula)

    def visit_predicate(self, formula: PredicateFormula) -> T:
        return self.generic_visit(formula)

    def visit_negation(self, formula: NegationFormula) -> T:
        return self.generic_visit(formula)

    def visit_connective(self, formula: ConnectiveFormula) -> T:
        return self.generic_visit(formula)

    def visit_quantifier(self, formula: QuantifierFormula) -> T:
        return self.generic_visit(formula)

    def generic_visit(self, formula: Formula) -> T:
        raise NotImplementedError


class FormulaTransformationVisitor(FormulaVisitor[Formula]):
    def visit_constant(self, formula: ConstantFormula) -> Formula:
        return formula

    def visit_equality(self, formula: EqualityFormula) -> Formula:
        return formula

    def visit_predicate(self, formula: PredicateFormula) -> Formula:
        return formula

    def visit_negation(self, formula: NegationFormula) -> Formula:
        return NegationFormula(self.visit(formula.sub))

    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        return ConnectiveFormula(
            formula.conn,
            self.visit(formula.a),
            self.visit(formula.b)
        )

    def visit_quantifier(self, formula: QuantifierFormula) -> Formula:
        return QuantifierFormula(
            formula.quantifier,
            formula.variable,
            self.visit(formula.sub)
        )


class TermSchemaVisitor[T]:
    def visit(self, schema: TermSchema) -> T:
        match schema:
            case VariablePlaceholder():
                return self.visit_variable_placeholder(schema)

            case TermPlaceholder():
                return self.visit_term_placeholder(schema)

            case FunctionTermSchema():
                return self.visit_function(schema)

    def visit_variable_placeholder(self, schema: VariablePlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_term_placeholder(self, schema: TermPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_function(self, schema: FunctionTermSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: TermSchema) -> T:
        raise NotImplementedError


class FormulaSchemaVisitor[T]:
    def visit(self, schema: ExtendedFormulaSchema) -> T:  # noqa: PLR0911
        match schema:
            case ConstantFormula():
                return self.visit_constant(schema)

            case EqualityFormulaSchema():
                return self.visit_equality(schema)

            case FormulaPlaceholder():
                return self.visit_formula_placeholder(schema)

            case NegationFormulaSchema():
                return self.visit_negation(schema)

            case ConnectiveFormulaSchema():
                return self.visit_connective(schema)

            case QuantifierFormulaSchema():
                return self.visit_quantifier(schema)

            case SubstitutionSchema():
                return self.visit(schema.formula)

    def visit_constant(self, schema: ConstantFormula) -> T:
        return self.generic_visit(schema)

    def visit_equality(self, schema: EqualityFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_formula_placeholder(self, schema: FormulaPlaceholder) -> T:
        return self.generic_visit(schema)

    def visit_negation(self, schema: NegationFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_connective(self, schema: ConnectiveFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_quantifier(self, schema: QuantifierFormulaSchema) -> T:
        return self.generic_visit(schema)

    def generic_visit(self, schema: FormulaSchema) -> T:
        raise NotImplementedError
