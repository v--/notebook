from ....polynomials.monomial import Monomial
from ....polynomials.polynomial.int import IntPolynomial
from ...terms import FunctionApplication, Term, Variable
from .signature import RING_SIGNATURE


ZERO_TERM = FunctionApplication(RING_SIGNATURE.get_function_symbol('0'), [])
ONE_TERM = FunctionApplication(RING_SIGNATURE.get_function_symbol('1'), [])
PLUS = RING_SIGNATURE.get_function_symbol('+')
MINUS = RING_SIGNATURE.get_function_symbol('-')
TIMES = RING_SIGNATURE.get_function_symbol('⋅')


def number_to_term(num: int) -> Term:
    if num == 0:
        return ZERO_TERM

    if num == 1:
        return ONE_TERM

    if num > 1:
        return FunctionApplication(PLUS, [
            ONE_TERM,
            number_to_term(num - 1)
        ])

    return FunctionApplication(MINUS, [number_to_term(-num)])


def monomial_to_term(mon: Monomial) -> Term:
    indeterminates = mon.get_indeterminates()

    if len(indeterminates) == 0:
        return ONE_TERM

    indet, *rest = indeterminates

    if len(rest) == 0 and mon[indet] == 1:
        return Variable(indet)

    return FunctionApplication(TIMES, [
        Variable(indet),
        monomial_to_term(
            Monomial({indet: mon[indet] - 1} | {ind: mon[ind] for ind in rest})
        )
    ])


# This is alg:integer_polynomial_to_logical_term in the monograph
def polynomial_to_term(pol: IntPolynomial) -> Term:
    monomials = pol.get_monomials()

    if len(monomials) == 0:
        return ZERO_TERM

    mon, *rest = monomials
    mon_term: Term

    if mon.degree == 0:
        mon_term = number_to_term(pol[mon])
    elif pol[mon] == 1:
        mon_term = monomial_to_term(mon)
    else:
        mon_term = FunctionApplication(TIMES, [
            number_to_term(pol[mon]),
            monomial_to_term(mon)
        ])

    if len(rest) == 0:
        return mon_term

    return FunctionApplication(PLUS, [
        mon_term,
        polynomial_to_term(IntPolynomial.from_mapping({m: pol[m] for m in rest}))
    ])
