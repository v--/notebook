from .terms import Variable, Application, Abstraction, Term
from .variables import new_variable, get_free_variables
from .substitution import substitute_in_term


# The assertions are needed because mypy doesn't handle such complicated type narrowing
def are_terms_alpha_equivalent(m: Term, n: Term) -> bool:
    match (m, n):
        case (Variable(), Variable()):
            assert isinstance(m, Variable) and isinstance(n, Variable)
            return m.name == n.name

        case (Application(), Application()):
            assert isinstance(m, Application) and isinstance(n, Application)
            return are_terms_alpha_equivalent(m.a, n.a) and are_terms_alpha_equivalent(m.b, n.b)

        case (Abstraction(), Abstraction()):
            assert isinstance(m, Abstraction) and isinstance(n, Abstraction)
            new_var = new_variable(m.var, get_free_variables(m.sub) | get_free_variables(n.sub))
            return are_terms_alpha_equivalent(
                substitute_in_term(m.sub, m.var, new_var),
                substitute_in_term(n.sub, n.var, new_var)
            )

        case _:
            return False


def disunify_free_bound_variables_impl(term: Term, context: set[Variable] = set()) -> Term:
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


def disunify_free_bound_variables(term: Term) -> Term:
    return disunify_free_bound_variables_impl(term, get_free_variables(term))
