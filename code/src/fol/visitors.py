from .terms import Variable, FunctionTerm, Term
from .formulas import Formula, EqualityFormula, PredicateFormula, NegationFormula, ConnectiveFormula, QuantifierFormula


class TermVisitor:
    def visit(self, term: Term):
        match term:
            case Variable():
                return self.visit_variable(term)

            case FunctionTerm():
                return self.visit_function(term)

    def visit_variable(self, term: Variable):
        return self.generic_visit(term)

    def visit_function(self, term: FunctionTerm):
        return self.generic_visit(term)

    def generic_visit(self, term: Term):
        raise NotImplementedError


class TermTransformationVisitor(TermVisitor):
    def visit_variable(self, term: Variable):
        return term

    def visit_function(self, term: FunctionTerm):
        return FunctionTerm(
            term.name,
            [self.visit(arg) for arg in term.arguments]
        )


class FormulaVisitor:
    def visit(self, formula: Formula):
        match formula:
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

    def visit_equality(self, formula: EqualityFormula):
        return self.generic_visit(formula)

    def visit_predicate(self, formula: PredicateFormula):
        return self.generic_visit(formula)

    def visit_negation(self, formula: NegationFormula):
        return self.generic_visit(formula)

    def visit_connective(self, formula: ConnectiveFormula):
        return self.generic_visit(formula)

    def visit_quantifier(self, formula: QuantifierFormula):
        return self.generic_visit(formula)

    def generic_visit(self, formula: Formula):
        raise NotImplementedError


class FormulaTransformationVisitor(FormulaVisitor):
    def visit_equality(self, formula: EqualityFormula):
        return formula

    def visit_predicate(self, formula: PredicateFormula):
        return formula

    def visit_negation(self, formula: NegationFormula):
        return NegationFormula(self.visit(formula.sub))

    def visit_connective(self, formula: ConnectiveFormula):
        return ConnectiveFormula(
            formula.conn,
            self.visit(formula.a),
            self.visit(formula.b)
        )

    def visit_quantifier(self, formula: QuantifierFormula):
        return QuantifierFormula(
            formula.quantifier,
            formula.variable,
            self.visit(formula.sub)
        )
