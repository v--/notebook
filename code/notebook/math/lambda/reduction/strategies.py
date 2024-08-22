from dataclasses import dataclass
from typing import Protocol

from ..terms import Abstraction, Application, LambdaTerm
from .exceptions import ReductionError


class Reduction(Protocol):
    def try_contract_redex(self, term: LambdaTerm) -> LambdaTerm | None:
        ...


class ReductionStrategy(Protocol):
    reduction: Reduction

    def try_reduce(self, term: LambdaTerm) -> LambdaTerm | None:
        ...


def reduce_term_once(term: LambdaTerm, strategy: ReductionStrategy) -> LambdaTerm:
    reduction = strategy.try_reduce(term)

    if reduction is None:
        raise ReductionError(f'Cannot β-reduce {reduction}')

    return reduction


def transitively_reduce_term(term: LambdaTerm, strategy: ReductionStrategy) -> LambdaTerm:
    reduction = term

    while next_reduction := strategy.try_reduce(reduction):
        reduction = next_reduction

    return reduction


@dataclass(frozen=True)
class NormalOrderStrategy(ReductionStrategy):
    reduction: Reduction

    def try_reduce(self, term: LambdaTerm) -> LambdaTerm | None:
        if contractum := self.reduction.try_contract_redex(term):
            return contractum

        if isinstance(term, Application):
            if a := self.try_reduce(term.a):
                return Application(a, term.b)

            if b := self.try_reduce(term.b):
                return Application(term.a, b)

        if isinstance(term, Abstraction) and (sub := self.try_reduce(term.sub)):
            return Abstraction(term.var, sub)

        return None


@dataclass(frozen=True)
class ApplicativeOrderStrategy(ReductionStrategy):
    reduction: Reduction

    def try_reduce(self, term: LambdaTerm) -> LambdaTerm | None:
        if isinstance(term, Application):
            if a := self.try_reduce(term.a):
                return Application(a, term.b)

            if b := self.try_reduce(term.b):
                return Application(term.a, b)

        if isinstance(term, Abstraction) and (sub := self.try_reduce(term.sub)):
            return Abstraction(term.var, sub)

        if contractum := self.reduction.try_contract_redex(term):
            return contractum

        return None
