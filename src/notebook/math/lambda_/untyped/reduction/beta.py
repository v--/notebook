import inspect
from typing import TYPE_CHECKING, override

from notebook.math.lambda_.terms import UntypedAbstraction, UntypedApplication, UntypedTerm
from notebook.math.lambda_.untyped.substitution import substitute
from notebook.support.coderefs import collector

from .strategies import Reduction


if TYPE_CHECKING:
    from collections.abc import Callable


class BetaReduction(Reduction):
    @override
    def try_contract_redex(self, term: UntypedTerm) -> UntypedTerm | None:
        if isinstance(term, UntypedApplication) and isinstance(term.left, UntypedAbstraction):
            return substitute(term.left.body, {term.left.var: term.right})

        return None


@collector.ref('alg:untyped_lambda_term_to_function')
def to_function(term: UntypedTerm) -> Callable:
    arg_names = list[str]()

    current = term
    while isinstance(current, UntypedAbstraction):
        arg_names.append(str(current.var.identifier))
        current = current.body

    def fun(*args: UntypedTerm) -> UntypedTerm:
        result = term
        i = 0

        while isinstance(result, UntypedAbstraction):
            result = substitute(result.body, {result.var: args[i]})
            i += 1

        return result

    parameters = [inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD) for name in arg_names]
    fun.__signature__ = inspect.signature(fun).replace(parameters=parameters)  # type: ignore[attr-defined]
    return fun
