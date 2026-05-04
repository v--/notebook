from inspect import Parameter, Signature
from typing import TYPE_CHECKING

from notebook.support.coderefs import collector

from .evaluation import evaluate_prop_formula
from .interpretation import PropInterpretation
from .variables import get_prop_variables


if TYPE_CHECKING:
    from collections.abc import Callable

    from .formulas import PropFormula


@collector.ref('def:parametrized_propositional_denotation')
def prop_formula_to_function(formula: PropFormula) -> Callable[..., bool]:
    variables = sorted(get_prop_variables(formula))
    signature = Signature(
        parameters=[Parameter(var.symbol.name, Parameter.POSITIONAL_OR_KEYWORD, annotation=bool) for var in variables],
        return_annotation=bool,
    )

    def function(*args: bool, **kwargs: bool) -> bool:
        bound = signature.bind(*args, **kwargs)
        interp = PropInterpretation(dict(zip(variables, bound.args, strict=True)))
        return evaluate_prop_formula(formula, interp)

    function.__signature__ = signature  # type: ignore[attr-defined]
    return function
