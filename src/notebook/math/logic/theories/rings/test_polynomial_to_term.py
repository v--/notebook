from .....support.pytest import pytest_parametrize_kwargs
from ....polynomials.polynomial.int import IntPolynomial, const, x, y
from ...parsing import parse_term
from .polynomial_to_term import polynomial_to_term
from .signature import RING_SIGNATURE
from .term_to_polynomial import term_to_polynomial


@pytest_parametrize_kwargs(
    dict(pol=const,      term='1'),
    dict(pol=-const,     term='-1'),
    dict(pol=x * y,      term='(x ⋅ y)'),
    dict(pol=2 * x ** 2, term='((1 + 1) ⋅ (x ⋅ x))'),
)
def test_polynomial_to_term(pol: IntPolynomial, term: str) -> None:
    term_ = parse_term(term, RING_SIGNATURE)
    assert polynomial_to_term(pol) == term_
    assert term_to_polynomial(term_) == pol


def test_grouping() -> None:
    src_term = parse_term('((x ⋅ x) + (x ⋅ x))', RING_SIGNATURE)
    dest_term = parse_term('((1 + 1) ⋅ (x ⋅ x))', RING_SIGNATURE)
    assert polynomial_to_term(term_to_polynomial(src_term)) == dest_term
