import functools
import itertools
from collections.abc import Callable
from dataclasses import dataclass
from typing import overload

from ....exceptions import UnreachableException
from ....parsing import iter_latin_identifiers
from ....support.unicode import itoa_superscripts
from ..alphabet import Quantifier
from ..formulas import Formula
from ..signature import FormalLogicSignature, FunctionSymbol, SignatureSymbol, SignatureSymbolNotation
from ..structure import FormalLogicStructure, VariableAssignment, evaluate_formula
from ..substitution import substitute_in_formula
from ..terms import FunctionApplication, Variable
from .exceptions import InvalidModelError
from .prefix import QuantifierPrefix
from .prenex_formula import PrenexFormula


@dataclass(frozen=True)
class SkolemConfiguration:
    prenex_formula: PrenexFormula
    signature: FormalLogicSignature


@dataclass(frozen=True)
class SkolemConfigurationWithModel[T](SkolemConfiguration):
    model: FormalLogicStructure[T]


def generate_new_function_name(signature: FormalLogicSignature, arity: int) -> str:
    for identifier in iter_latin_identifiers():
        candidate = str(identifier) + itoa_superscripts(arity)

        if candidate not in signature:
            return candidate

    raise UnreachableException


def skolem_function_interpretation[T](
    matrix: Formula,
    active_var: Variable,
    model: FormalLogicStructure[T],
    prefix: QuantifierPrefix,
    suffix: QuantifierPrefix,
    *args: T
) -> T:
    assignment = VariableAssignment[T]()

    for (_, v), arg in zip(prefix, args, strict=True):
        assignment = assignment.modify(v, arg)

    for tup in itertools.product(model.universe, repeat=len(suffix)):
        for (_, v), arg in zip(suffix, tup, strict=True):
            assignment = assignment.modify(v, arg)

        if evaluate_formula(matrix, model, assignment):
            return assignment.get_value(active_var)

    raise InvalidModelError('The provided structure is not a model')


@overload
def skolemize(formula: PrenexFormula, signature: FormalLogicSignature) -> SkolemConfiguration: ...
@overload
def skolemize[T](formula: PrenexFormula, signature: FormalLogicSignature, model: FormalLogicStructure[T]) -> SkolemConfigurationWithModel[T]: ...
def skolemize[T](formula: PrenexFormula, signature: FormalLogicSignature, model: FormalLogicStructure[T] | None = None) -> SkolemConfiguration:
    universal_prefix = QuantifierPrefix()
    matrix = formula.matrix
    expanded_model = model
    extended_signature = FormalLogicSignature(*signature)

    for k, (quant, var) in enumerate(formula.prefix):
        match quant:
            case Quantifier.UNIVERSAL:
                universal_prefix.append(quant, var)

            case Quantifier.EXISTENTIAL:
                arity = len(universal_prefix)
                new_symbol = FunctionSymbol(
                    generate_new_function_name(extended_signature, arity),
                    arity,
                    SignatureSymbolNotation.PREFIX
                )

                extended_signature.add_symbol(new_symbol)

                if expanded_model:
                    interpretation: dict[SignatureSymbol, Callable[..., T]] = {
                        sym: functools.partial(expanded_model.apply, sym)
                        for sym in expanded_model.signature
                    }

                    interpretation[new_symbol] = functools.partial(
                        skolem_function_interpretation,
                        matrix, var, expanded_model, universal_prefix, QuantifierPrefix(list(formula.prefix)[k:])
                    )

                    expanded_model = FormalLogicStructure(
                        extended_signature,
                        expanded_model.universe,
                        interpretation
                    )

                matrix = substitute_in_formula(matrix, {
                    var: FunctionApplication(new_symbol, [v for _, v in universal_prefix])
                })

    resulting_formula = PrenexFormula(universal_prefix, matrix)

    if expanded_model:
        return SkolemConfigurationWithModel(resulting_formula, extended_signature, expanded_model)

    return SkolemConfiguration(resulting_formula, extended_signature)
