from .formulas import (
    ConnectiveFormula,
    ConstantFormula,
    EqualityFormula,
    Formula,
    NegationFormula,
    PredicateFormula,
    QuantifierFormula,
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
        return NegationFormula(self.visit(formula.body))

    def visit_connective(self, formula: ConnectiveFormula) -> Formula:
        return ConnectiveFormula(
            formula.conn,
            self.visit(formula.left),
            self.visit(formula.right)
        )

    def visit_quantifier(self, formula: QuantifierFormula) -> Formula:
        return QuantifierFormula(
            formula.quantifier,
            formula.var,
            self.visit(formula.body)
        )
