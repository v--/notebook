from collections.abc import Collection

from ..terms import Constant, UntypedAbstraction, UntypedApplication, UntypedTerm, Variable
from ..variables import get_free_variables, new_variable
from .substitution import substitute


# The assertions are needed because mypy doesn't handle such complicated type narrowing
def are_terms_alpha_equivalent(m: UntypedTerm, n: UntypedTerm) -> bool:
    match (m, n):
        case (Variable(), Variable()):
            assert isinstance(m, Variable)
            assert isinstance(n, Variable)
            return m.identifier == n.identifier

        case (UntypedApplication(), UntypedApplication()):
            assert isinstance(m, UntypedApplication)
            assert isinstance(n, UntypedApplication)
            return are_terms_alpha_equivalent(m.a, n.a) and are_terms_alpha_equivalent(m.b, n.b)

        case (UntypedAbstraction(), UntypedAbstraction()):
            assert isinstance(m, UntypedAbstraction)
            assert isinstance(n, UntypedAbstraction)

            if m.var == n.var:
                return are_terms_alpha_equivalent(m.sub, n.sub)

            return m.var not in get_free_variables(n.sub) and \
                are_terms_alpha_equivalent(m.sub, substitute(n.sub, variable_mapping={n.var: m.var}))

        case _:
            return False


# This is alg:separation_of_free_and_bound_variables in the monograph
def separate_free_and_bound_variables_impl(term: UntypedTerm, context: Collection[Variable] = set()) -> UntypedTerm:
    match term:
        case Constant():
            return term

        case Variable():
            return term

        case UntypedApplication():
            return UntypedApplication(
                separate_free_and_bound_variables_impl(term.a, context),
                separate_free_and_bound_variables_impl(term.b, context)
            )

        case UntypedAbstraction():
            if term.var not in context:
                return UntypedAbstraction(term.var, separate_free_and_bound_variables_impl(term.sub, {*context, term.var}))

            new_var = new_variable(context)

            return UntypedAbstraction(
                new_var,
                substitute(
                    separate_free_and_bound_variables_impl(term.sub, {*context, new_var}),
                    {term.var: new_var}
                ),
            )


def separate_free_and_bound_variables(term: UntypedTerm) -> UntypedTerm:
    return separate_free_and_bound_variables_impl(term, get_free_variables(term))
