from dataclasses import dataclass
from typing import Protocol

from ...terms import UntypedAbstraction, UntypedApplication, UntypedTerm
from .exceptions import ReductionError


class Reduction(Protocol):
    def try_contract_redex(self, term: UntypedTerm) -> UntypedTerm | None:
        ...


class ReductionStrategy(Protocol):
    reduction: Reduction

    def try_reduce(self, term: UntypedTerm) -> UntypedTerm | None:
        ...


def reduce_term_once(term: UntypedTerm, strategy: ReductionStrategy) -> UntypedTerm:
    reduction = strategy.try_reduce(term)

    if reduction is None:
        raise ReductionError(f'Cannot reduce {reduction}')

    return reduction


def transitively_reduce_term(term: UntypedTerm, strategy: ReductionStrategy) -> UntypedTerm:
    reduction = term

    while next_reduction := strategy.try_reduce(reduction):
        reduction = next_reduction

    return reduction


@dataclass(frozen=True)
class NormalOrderStrategy(ReductionStrategy):
    reduction: Reduction

    def try_reduce(self, term: UntypedTerm) -> UntypedTerm | None:
        if contractum := self.reduction.try_contract_redex(term):
            return contractum

        if isinstance(term, UntypedApplication):
            if a := self.try_reduce(term.a):
                return UntypedApplication(a, term.b)

            if b := self.try_reduce(term.b):
                return UntypedApplication(term.a, b)

        if isinstance(term, UntypedAbstraction) and (sub := self.try_reduce(term.sub)):
            return UntypedAbstraction(term.var, sub)

        return None


@dataclass(frozen=True)
class ApplicativeOrderStrategy(ReductionStrategy):
    reduction: Reduction

    def try_reduce(self, term: UntypedTerm) -> UntypedTerm | None:
        if isinstance(term, UntypedApplication):
            if a := self.try_reduce(term.a):
                return UntypedApplication(a, term.b)

            if b := self.try_reduce(term.b):
                return UntypedApplication(term.a, b)

        if isinstance(term, UntypedAbstraction) and (sub := self.try_reduce(term.sub)):
            return UntypedAbstraction(term.var, sub)

        if contractum := self.reduction.try_contract_redex(term):
            return contractum

        return None
