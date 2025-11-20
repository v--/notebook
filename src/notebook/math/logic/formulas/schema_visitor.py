from .schemas import (
    ConnectiveFormulaSchema,
    ConstantFormula,
    EqualityFormulaSchema,
    FormulaPlaceholder,
    FormulaSchema,
    NegationFormulaSchema,
    PredicateApplicationSchema,
    QuantifierFormulaSchema,
)


class FormulaSchemaVisitor[T]:
    def visit(self, schema: FormulaSchema) -> T:
        match schema:
            case ConstantFormula():
                return self.visit_constant(schema)

            case EqualityFormulaSchema():
                return self.visit_equality(schema)

            case PredicateApplicationSchema():
                return self.visit_predicate(schema)

            case FormulaPlaceholder():
                return self.visit_formula_placeholder(schema)

            case NegationFormulaSchema():
                return self.visit_negation(schema)

            case ConnectiveFormulaSchema():
                return self.visit_connective(schema)

            case QuantifierFormulaSchema():
                return self.visit_quantifier(schema)

    def visit_logical_constant(self, schema: ConstantFormula) -> T:
        return self.generic_visit(schema)

    def visit_equality(self, schema: EqualityFormulaSchema) -> T:
        return self.generic_visit(schema)

    def visit_predicate(self, schema: PredicateApplicationSchema) -> T:
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
