import inspect
from collections.abc import Callable

from ...substitution import TermSubstitution, apply_term_substitution
from ...terms import Abstraction, Application, LambdaTerm
from .strategies import Reduction


class BetaReduction(Reduction):
    def try_contract_redex(self, term: LambdaTerm) -> LambdaTerm | None:
        if isinstance(term, Application) and isinstance(term.a, Abstraction):
            return apply_term_substitution(term.a.sub, TermSubstitution({ term.a.var: term.b }))

        return None


def to_function(term: LambdaTerm) -> Callable:
    red = BetaReduction()
    arg_names = list[str]()

    current = term
    while isinstance(current, Abstraction):
        arg_names.append(str(current.var.identifier))
        current = current.sub

    def fun(*args: LambdaTerm) -> LambdaTerm:
        result = term
        i = 0

        while isinstance(result, Abstraction):
            reduced = red.try_contract_redex(Application(result, args[i]))
            assert reduced
            result = reduced
            i += 1

        return result

    parameters = [inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD) for name in arg_names]
    fun.__signature__ = inspect.signature(fun).replace(parameters=parameters)  # type: ignore[attr-defined]
    return fun
