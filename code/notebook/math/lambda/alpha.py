from .substitution import Substitution, apply_substitution
from .terms import Abstraction, Application, LambdaTerm, Variable
from .variables import get_free_variables, new_variable


# The assertions are needed because mypy doesn't handle such complicated type narrowing
def are_terms_alpha_equivalent(m: LambdaTerm, n: LambdaTerm) -> bool:
    match (m, n):
        case (Variable(), Variable()):
            assert isinstance(m, Variable)
            assert isinstance(n, Variable)
            return m.identifier == n.identifier

        case (Application(), Application()):
            assert isinstance(m, Application)
            assert isinstance(n, Application)
            return are_terms_alpha_equivalent(m.a, n.a) and are_terms_alpha_equivalent(m.b, n.b)

        case (Abstraction(), Abstraction()):
            assert isinstance(m, Abstraction)
            assert isinstance(n, Abstraction)
            new_var = new_variable(get_free_variables(m.sub) | get_free_variables(n.sub))
            return are_terms_alpha_equivalent(
                apply_substitution(m.sub, Substitution({m.var: new_var})),
                apply_substitution(n.sub, Substitution({n.var: new_var}))
            )

        case _:
            return False


def disunify_free_bound_variables_impl(term: LambdaTerm, context: frozenset[Variable] = frozenset()) -> LambdaTerm:
    match term:
        case Variable():
            return term

        case Application():
            return Application(
                disunify_free_bound_variables_impl(term.a, context),
                disunify_free_bound_variables_impl(term.b, context)
            )

        case Abstraction():
            new_var = new_variable(context) if term.var in context else term.var

            return Abstraction(
                new_var,
                apply_substitution(
                    disunify_free_bound_variables_impl(term.sub, context | {new_var}),
                    Substitution({term.var: new_var})
                ),
            )


def disunify_free_bound_variables(term: LambdaTerm) -> LambdaTerm:
    return disunify_free_bound_variables_impl(term, get_free_variables(term))
