from collections.abc import Collection

from ..substitution import TermSubstitution, apply_term_substitution
from ..terms import Abstraction, Application, Constant, LambdaTerm, Variable
from ..variables import get_free_variables, new_variable


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

            if m.var == n.var:
                return are_terms_alpha_equivalent(m.sub, n.sub)

            return m.var not in get_free_variables(n.sub) and \
                are_terms_alpha_equivalent(m.sub, apply_term_substitution(n.sub, TermSubstitution({n.var: m.var})))

        case _:
            return False


# This is alg:separation_of_free_and_bound_variables in the monograph
def separate_free_and_bound_variables_impl(term: LambdaTerm, context: Collection[Variable] = set()) -> LambdaTerm:
    match term:
        case Constant():
            return term

        case Variable():
            return term

        case Application():
            return Application(
                separate_free_and_bound_variables_impl(term.a, context),
                separate_free_and_bound_variables_impl(term.b, context)
            )

        case Abstraction():
            if term.var not in context:
                return Abstraction(term.var, separate_free_and_bound_variables_impl(term.sub, {*context, term.var}))

            new_var = new_variable(context)

            return Abstraction(
                new_var,
                apply_term_substitution(
                    separate_free_and_bound_variables_impl(term.sub, {*context, new_var}),
                    TermSubstitution({term.var: new_var})
                ),
            )


def separate_free_and_bound_variables(term: LambdaTerm) -> LambdaTerm:
    return separate_free_and_bound_variables_impl(term, get_free_variables(term))
