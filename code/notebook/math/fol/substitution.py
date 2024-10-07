from .formulas import EqualityFormula, Formula, PredicateFormula, QuantifierFormula
from .terms import FunctionTerm, Term, Variable
from .variables import get_free_variables, get_term_variables, new_variable
from .visitors import FormulaTransformationVisitor, TermTransformationVisitor


class TermSubstitutionVisitor(TermTransformationVisitor):
    from_term: Term
    to_term: Term

    def __init__(self, from_term: Term, to_term: Term) -> None:
        self.from_term = from_term
        self.to_term = to_term

    def visit_variable(self, term: Variable) -> Term:
        if term == self.from_term:
            return self.to_term

        return term

    def visit_function(self, term: FunctionTerm) -> Term:
        if term == self.from_term:
            return self.to_term

        return FunctionTerm(term.name, [self.visit(arg) for arg in term.arguments])


def substitute_in_term(term: Term, from_term: Term, to_term: Term) -> Term:
    return TermSubstitutionVisitor(from_term, to_term).visit(term)


class FormulaSubstitutionVisitor(FormulaTransformationVisitor):
    def __init__(self, from_term: Term, to_term: Term) -> None:
        self.from_term = from_term
        self.to_term = to_term
        super().__init__()

    def visit_equality(self, formula: EqualityFormula) -> EqualityFormula:
        term_visitor = TermSubstitutionVisitor(self.from_term, self.to_term)
        return EqualityFormula(term_visitor.visit(formula.a), term_visitor.visit(formula.b))

    def visit_predicate(self, formula: PredicateFormula) -> PredicateFormula:
        term_visitor = TermSubstitutionVisitor(self.from_term, self.to_term)
        return PredicateFormula(formula.name, [term_visitor.visit(arg) for arg in formula.arguments])

    def visit_quantifier(self, formula: QuantifierFormula) -> QuantifierFormula:
        free_from = get_term_variables(self.from_term)
        free_to = get_term_variables(self.to_term)

        # This first check is not strictly necessary, but it is how we defined the algorithm
        if formula.variable in free_from:
            return formula

        if formula.variable not in {*free_from, *free_to}:
            return QuantifierFormula(
                formula.quantifier,
                formula.variable,
                self.visit(formula.sub)
            )

        new_var = new_variable({*free_from, *free_to, *get_free_variables(formula.sub)})
        sub_visitor = FormulaSubstitutionVisitor(formula.variable, new_var)

        return QuantifierFormula(
            formula.quantifier,
            new_var,
            self.visit(sub_visitor.visit(formula.sub))
        )


def substitute_in_formula(formula: Formula, from_term: Term, to_term: Term) -> Formula:
    return FormulaSubstitutionVisitor(from_term, to_term).visit(formula)
