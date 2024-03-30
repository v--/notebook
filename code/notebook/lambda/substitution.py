from .terms import Variable, Abstraction, Term
from .visitors import TermTransformationVisitor
from .variables import new_variable, get_free_variables


# This is def:lambda_substitution in the text
class TermSubstitutionVisitor(TermTransformationVisitor):
    var: Variable
    rep: Term

    def __init__(self, var: Variable, rep: Term):
        self.var = var
        self.rep = rep

    def visit_variable(self, term: Variable):
        return self.rep if term == self.var else term

    def visit_abstraction(self, term: Abstraction):
        if term.var == self.var:
            return term

        free_sub = get_free_variables(term.sub)

        if self.var not in free_sub:
            return term

        free_rep = get_free_variables(self.rep)

        if term.var not in free_rep:
            return Abstraction(term.var, self.visit(term.sub))

        new_var = new_variable(term.var, free_rep | free_sub)
        sub_visitor = TermSubstitutionVisitor(term.var, new_var)

        return Abstraction(
            new_var,
            self.visit(sub_visitor.visit(term.sub))
        )


def substitute_in_term(term: Term, var: Variable, replacement: Term):
    return TermSubstitutionVisitor(var, replacement).visit(term)
