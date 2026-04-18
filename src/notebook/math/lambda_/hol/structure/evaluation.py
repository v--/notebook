# ruff: noqa: FURB118
import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .....exceptions import UnreachableException
from .....support.coderefs import collector
from ...alphabet import BinaryTypeConnective
from ...assertions import VariableTypeAssertion
from ...terms import Constant, TypedAbstraction, TypedApplication, TypedTerm, Variable
from ...types import BaseType, SimpleConnectiveType, SimpleType
from .. import common
from ..signature import NonLogicalConstantSymbol, SortSymbol
from .assignment import HolVariableAssignment
from .exceptions import HolInterpretationError, MissingInterpretationError


if TYPE_CHECKING:
    from collections.abc import Iterable

    from ...type_context import TypeContext
    from ..expression import HolExpression
    from .structure import HolStructure, HolStructureValue


def iter_type_values[T](type_: SimpleType, structure: HolStructure[T]) -> Iterable[HolStructureValue[T]]:
    if isinstance(type_, BaseType):
        sym = type_.value

        match sym:
            case common.prop.value:
                yield True
                yield False

            case SortSymbol():
                if sym not in structure.sort_universes:
                    raise MissingInterpretationError(f'Missing interpretation for sort {sym}')

                yield from structure.sort_universes[sym]

            case _:
                raise HolInterpretationError(f'Unrecognized symbol {sym}')

    if isinstance(type_, SimpleConnectiveType):
        if type_.conn != BinaryTypeConnective.ARROW:
            raise HolInterpretationError('Only arrow types are allowed')

        domain = list(iter_type_values(type_.left, structure))
        codomain = list(iter_type_values(type_.right, structure))

        for tup in itertools.product(codomain, repeat=len(domain)):
            fun_mapping = dict(zip(domain, tup, strict=True))
            yield fun_mapping.__getitem__


@dataclass(frozen=True)
class HolBinderEvaluator[T]:
    term: TypedAbstraction
    context: TypeContext
    structure: HolStructure[T]
    assignment: HolVariableAssignment[T]

    def get_domain(self) -> Iterable[HolStructureValue[T]]:
        return list(iter_type_values(self.term.var_type, self.structure))

    def __call__(self, value: HolStructureValue[T]) -> HolStructureValue[T]:
        assertion = VariableTypeAssertion(self.term.var, self.term.var_type)
        return evaluate_hol_term(
            self.term.body,
            self.context.modify(self.term.var, self.term.var_type),
            self.structure,
            self.assignment.modify(assertion, value),
        )


# We suppose that only well-typed expressions reach this point.
def evaluate_hol_term[T](  # noqa: C901
    term: TypedTerm,
    context: TypeContext,
    structure: HolStructure[T],
    assignment: HolVariableAssignment[T],
) -> HolStructureValue[T]:
    match term:
        case Variable():
            return assignment.get_value(term, context[term])

        case common.verum:
            return True

        case common.falsum:
            return False

        case common.negation:
            return lambda p: not p

        case common.conjunction:
            return lambda p: (lambda q: p and q)

        case common.disjunction:
            return lambda p: (lambda q: p and q)

        case common.conditional:
            return lambda p: (lambda q: not p or q)

        case common.biconditional:
            return lambda p: (lambda q: p == q)

        case common.equality:
            return lambda x: (lambda y: x == y)

        case common.forall:
            return lambda pred: min(pred(x) for x in pred.get_domain())

        case common.exists:
            return lambda pred: max(pred(x) for x in pred.get_domain())

        case Constant() if isinstance(term.value, NonLogicalConstantSymbol):
            return structure.interpretation[term.value]

        case Constant():
            raise HolInterpretationError(f'Unexpected {term.value.get_kind_string()} {term.value}')

        case TypedApplication():
            fun = evaluate_hol_term(term.left, context, structure, assignment)

            if TYPE_CHECKING:
                assert callable(fun)

            arg = evaluate_hol_term(term.right, context, structure, assignment)
            return fun(arg)

        case TypedAbstraction():
            return HolBinderEvaluator(term, context, structure, assignment)

    raise UnreachableException


@collector.ref('alg:hol_denotation')
def evaluate_hol_expression[T](
    expression: HolExpression,
    structure: HolStructure[T],
    assignment: HolVariableAssignment[T] | None = None,
) -> HolStructureValue[T]:
    return evaluate_hol_term(
        expression.term,
        expression.context,
        structure,
        assignment or HolVariableAssignment(),
    )
