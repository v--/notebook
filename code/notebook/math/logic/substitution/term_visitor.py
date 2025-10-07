from ..terms import FunctionTerm, Term, TermTransformationVisitor, Variable


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
