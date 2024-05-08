from .terms import Abstraction, LambdaTerm, Variable
from .variables import get_free_variables, new_variable
from .visitors import TermTransformationVisitor


# This is def:uniform_lambda_substitution in the monograph
class TermSubstitutionVisitor(TermTransformationVisitor):
    var: Variable
    rep: LambdaTerm

    def __init__(self, var: Variable, rep: LambdaTerm) -> None:
        self.var = var
        self.rep = rep

    def visit_variable(self, term: Variable) -> LambdaTerm:
        return self.rep if term == self.var else term

    def visit_abstraction(self, term: Abstraction) -> Abstraction:
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


def substitute_in_term(term: LambdaTerm, var: Variable, replacement: LambdaTerm) -> LambdaTerm:
    return TermSubstitutionVisitor(var, replacement).visit(term)
