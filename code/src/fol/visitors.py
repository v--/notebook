from .types import Variable, FunctionTerm, Term, Formula, EqualityFormula, PredicateFormula, NegationFormula, ConnectiveFormula, QuantifierFormula, Formula


class TermVisitor:
    def visit(self, term: Term):
        if isinstance(term, Variable):
            return self.visit_variable(term)

        if isinstance(term, FunctionTerm):
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
        if isinstance(formula, EqualityFormula):
            return self.visit_equality(formula)

        if isinstance(formula, PredicateFormula):
            return self.visit_predicate(formula)

        if isinstance(formula, NegationFormula):
            return self.visit_negation(formula)

        if isinstance(formula, ConnectiveFormula):
            return self.visit_connective(formula)

        if isinstance(formula, QuantifierFormula):
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
