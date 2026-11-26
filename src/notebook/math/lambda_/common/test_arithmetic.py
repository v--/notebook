from notebook.math.lambda_.terms import UntypedApplication
from notebook.math.lambda_.terms.terms import UntypedAbstraction, UntypedTerm
from notebook.math.lambda_.untyped.reduction.api import fully_reduce_term

from .arithmetic import church_numeral_to_int, int_to_church_numeral, is_even, succ
from .logic import is_term_falsy, is_term_truthy


def test_applicative_beta_numerals(ceiling: int = 10) -> None:
    numeral: UntypedTerm = int_to_church_numeral(0)

    for n in range(ceiling):
        numeral = fully_reduce_term(UntypedApplication(succ, numeral), eta=False)
        assert isinstance(numeral, UntypedAbstraction)
        assert church_numeral_to_int(numeral) == n


def test_applicative_beta_numerals_is_even(ceiling: int = 10) -> None:
    numeral: UntypedTerm = int_to_church_numeral(0)

    for n in range(ceiling):
        result = fully_reduce_term(UntypedApplication(is_even, numeral), eta=False)

        if n % 2 == 0:
            is_term_truthy(result)
        else:
            is_term_falsy(result)
