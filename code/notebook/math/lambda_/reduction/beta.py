import inspect
from collections.abc import Callable

from ..substitution import TermSubstitution, apply_term_substitution
from ..terms import UntypedAbstraction, UntypedApplication, UntypedTerm
from .strategies import Reduction


class BetaReduction(Reduction):
    def try_contract_redex(self, term: UntypedTerm) -> UntypedTerm | None:
        if isinstance(term, UntypedApplication) and isinstance(term.a, UntypedAbstraction):
            return apply_term_substitution(term.a.sub, TermSubstitution(variable_mapping={ term.a.var: term.b }))

        return None


def to_function(term: UntypedTerm) -> Callable:
    red = BetaReduction()
    arg_names = list[str]()

    current = term
    while isinstance(current, UntypedAbstraction):
        arg_names.append(str(current.var.identifier))
        current = current.sub

    def fun(*args: UntypedTerm) -> UntypedTerm:
        result = term
        i = 0

        while isinstance(result, UntypedAbstraction):
            reduced = red.try_contract_redex(UntypedApplication(result, args[i]))
            assert reduced
            result = reduced
            i += 1

        return result

    parameters = [inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD) for name in arg_names]
    fun.__signature__ = inspect.signature(fun).replace(parameters=parameters)  # type: ignore[attr-defined]
    return fun
