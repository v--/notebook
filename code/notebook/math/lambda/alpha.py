from typing import Optional

from .substitution import substitute_in_term
from .terms import Abstraction, Application, LambdaTerm, Variable
from .variables import get_free_variables, new_variable


# The assertions are needed because mypy doesn't handle such complicated type narrowing
def are_terms_alpha_equivalent(m: LambdaTerm, n: LambdaTerm) -> bool:
    match (m, n):
        case (Variable(), Variable()):
            assert isinstance(m, Variable)
            assert isinstance(n, Variable)
            return m.name == n.name

        case (Application(), Application()):
            assert isinstance(m, Application)
            assert isinstance(n, Application)
            return are_terms_alpha_equivalent(m.a, n.a) and are_terms_alpha_equivalent(m.b, n.b)

        case (Abstraction(), Abstraction()):
            assert isinstance(m, Abstraction)
            assert isinstance(n, Abstraction)
            new_var = new_variable(m.var, get_free_variables(m.sub) | get_free_variables(n.sub))
            return are_terms_alpha_equivalent(
                substitute_in_term(m.sub, m.var, new_var),
                substitute_in_term(n.sub, n.var, new_var)
            )

        case _:
            return False


def disunify_free_bound_variables_impl(term: LambdaTerm, context: Optional[set[Variable]] = None) -> LambdaTerm:
    if context is None:
        context = set()
    match term:
        case Variable():
            return term

        case Application():
            return Application(
                disunify_free_bound_variables_impl(term.a, context),
                disunify_free_bound_variables_impl(term.b, context)
            )

        case Abstraction():
            new_var = new_variable(term.var, context)

            return Abstraction(
                new_var,
                substitute_in_term(
                    disunify_free_bound_variables_impl(term.sub, context | {new_var}),
                    term.var,
                    new_var
                ),
            )


def disunify_free_bound_variables(term: LambdaTerm) -> LambdaTerm:
    return disunify_free_bound_variables_impl(term, get_free_variables(term))
