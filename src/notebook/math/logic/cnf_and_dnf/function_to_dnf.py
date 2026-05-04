import inspect
from typing import TYPE_CHECKING

from notebook.math.logic.alphabet import BinaryConnective, PropConstantSymbol
from notebook.math.logic.formulas import PropConstant
from notebook.math.logic.propositional import (
    DEFAULT_PROP_SIGNATURE,
    PropConnectiveFormula,
    PropFormula,
    PropNegationFormula,
    PropVariable,
    iter_interpretations_for_variables,
)
from notebook.support.coderefs import collector

from .exceptions import VariableNameError


if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


def vararg_connect(conn: BinaryConnective, formulas: Iterable[PropFormula]) -> PropFormula:
    head, *tail = formulas

    if len(tail) == 0:
        return head

    return PropConnectiveFormula(conn, head, vararg_connect(conn, tail))


def function_params_as_variables(fun: Callable[..., bool]) -> Iterable[PropVariable]:
    for param in inspect.signature(fun).parameters.values():
        try:
            yield DEFAULT_PROP_SIGNATURE.get_prop_variable(param.name)
        except KeyError:
            raise VariableNameError(f'The parameter name {param.name!r} is not a valid propositional variable name.') from None


@collector.ref('alg:function_to_dnf')
def function_to_dnf(fun: Callable[..., bool]) -> PropFormula:
    variables = list(function_params_as_variables(fun))

    if len(variables) == 0:
        return PropConstant(PropConstantSymbol.VERUM if fun() else PropConstantSymbol.FALSUM)

    disjuncts = list[PropFormula](
        vararg_connect(BinaryConnective.CONJUNCTION, [
            var if value else PropNegationFormula(var) for var, value in interp.iter_items()
        ])
        for interp in iter_interpretations_for_variables(variables)
        if fun(**interp.get_kwargs())
    )

    match disjuncts:
        case []:
            return PropConstant(PropConstantSymbol.FALSUM)

        case [disjunct]:
            return disjunct

        case _:
            return vararg_connect(BinaryConnective.DISJUNCTION, disjuncts)
