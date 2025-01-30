from dataclasses import dataclass
from typing import Protocol

from ..terms import Abstraction, Application, Term
from .exceptions import ReductionError


class Reduction(Protocol):
    def try_contract_redex(self, term: Term) -> Term | None:
        ...


class ReductionStrategy(Protocol):
    reduction: Reduction

    def try_reduce(self, term: Term) -> Term | None:
        ...


def reduce_term_once(term: Term, strategy: ReductionStrategy) -> Term:
    reduction = strategy.try_reduce(term)

    if reduction is None:
        raise ReductionError(f'Cannot β-reduce {reduction}')

    return reduction


def transitively_reduce_term(term: Term, strategy: ReductionStrategy) -> Term:
    reduction = term

    while next_reduction := strategy.try_reduce(reduction):
        reduction = next_reduction

    return reduction


@dataclass(frozen=True)
class NormalOrderStrategy(ReductionStrategy):
    reduction: Reduction

    def try_reduce(self, term: Term) -> Term | None:
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

    def try_reduce(self, term: Term) -> Term | None:
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
