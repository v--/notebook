# ruff: noqa: FURB118

import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ....exceptions import UnreachableException
from ..alphabet import BinaryTypeConnective
from ..assertions import VariableTypeAssertion
from ..terms import Constant, TypedAbstraction, TypedApplication, TypedTerm, Variable
from ..types import BaseType, SimpleConnectiveType, SimpleType
from .assignment import HolVariableAssignment
from .exceptions import LambdaInterpretationError, MissingInterpretationError
from .signature import NonLogicalConstantSymbol, SortSymbol, common_constants, common_types


if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from .expressions import HolExpression
    from .structure import HolStructure, HolStructureValue


def iter_type_values[T](type_: SimpleType, structure: HolStructure[T]) -> Iterable[HolStructureValue[T]]:
    if isinstance(type_, BaseType):
        sym = type_.value

        match sym:
            case common_types.prop:
                yield True
                yield False

            case SortSymbol():
                if sym not in structure.sort_universes:
                    raise MissingInterpretationError(f'Missing interpretation for sort {sym}')

                yield from structure.sort_universes[sym]

            case _:
                raise LambdaInterpretationError(f'Unrecognized symbol {sym}')

    if isinstance(type_, SimpleConnectiveType):
        if type_.conn != BinaryTypeConnective.ARROW:
                raise LambdaInterpretationError('Only arrow types are allowed')

        domain = list(iter_type_values(type_.left, structure))
        codomain = list(iter_type_values(type_.right, structure))

        for tup in itertools.product(codomain, repeat=len(domain)):
            fun_mapping = dict(zip(domain, tup, strict=True))
            yield fun_mapping.__getitem__


@dataclass(frozen=True)
class HolBinderEvaluator[T]:
    term: TypedAbstraction
    context: Sequence[VariableTypeAssertion]
    structure: HolStructure[T]
    assignment: HolVariableAssignment[T]

    def get_domain(self) -> Iterable[HolStructureValue[T]]:
        return list(iter_type_values(self.term.var_type, self.structure))

    def __call__(self, value: HolStructureValue[T]) -> HolStructureValue[T]:
        assertion = VariableTypeAssertion(self.term.var, self.term.var_type)

        return evaluate_hol_term(
            self.term.body,
            [*self.context, assertion],
            self.structure,
            self.assignment.modify(assertion, value),
        )


# We suppose that only well-typed expressions reach this point.
def evaluate_hol_term[T](  # noqa: C901
    term: TypedTerm,
    context: Sequence[VariableTypeAssertion],
    structure: HolStructure[T],
    assignment: HolVariableAssignment[T],
) -> HolStructureValue[T]:
    if isinstance(term, Variable):
        return assignment.get_value(next(assertion for assertion in context if assertion.term == term))

    if isinstance(term, Constant):
        match term.value:
            case common_constants.verum:
                return True

            case common_constants.falsum:
                return False

            case common_constants.negation:
                return lambda p: not p

            case common_constants.conjunction:
                return lambda p: (lambda q: p and q)

            case common_constants.disjunction:
                return lambda p: (lambda q: p and q)

            case common_constants.conditional:
                return lambda p: (lambda q: not p or q)

            case common_constants.biconditional:
                return lambda p: (lambda q: p == q)

            case common_constants.equality:
                return lambda x: (lambda y: x == y)

            case common_constants.forall:
                return lambda pred: min(pred(x) for x in pred.get_domain())

            case common_constants.exists:
                return lambda pred: max(pred(x) for x in pred.get_domain())

            case NonLogicalConstantSymbol():
                return structure.interpretation[term.value]

            case _:
                raise LambdaInterpretationError(f'Unexpected {term.value.get_kind_string()} {term.value}')

    if isinstance(term, TypedApplication):
        fun = evaluate_hol_term(term.left, context, structure, assignment)
        assert callable(fun)  # noqa: S101
        arg = evaluate_hol_term(term.right, context, structure, assignment)
        return fun(arg)

    if isinstance(term, TypedAbstraction):
        return HolBinderEvaluator(term, context, structure, assignment)

    raise UnreachableException


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
