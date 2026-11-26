from notebook.math.lambda_.untyped.reduction.beta import BetaReduction
from notebook.math.lambda_.untyped.reduction.eta import EtaReduction, Reduction
from notebook.math.lambda_.untyped.reduction.strategies import NormalOrderStrategy, transitively_reduce_term
lazy from notebook.math.lambda_.terms.terms import UntypedTerm


def fully_reduce_term(term: UntypedTerm, *, beta: bool = True, eta: bool = True) -> UntypedTerm:
    reductions: list[Reduction] = []

    if beta:
        reductions.append(BetaReduction())

    if eta:
        reductions.append(EtaReduction())

    return transitively_reduce_term(term, *(NormalOrderStrategy(red) for red in reductions))
