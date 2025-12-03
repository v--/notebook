from dataclasses import dataclass
from typing import override

from ....polynomials.monomial import Monomial
from ....polynomials.polynomial.int import IntPolynomial, const, zero
from ...terms import FunctionApplication, Term, TermVisitor, Variable
from ..exceptions import UnrecognizedSymbolError


@dataclass(frozen=True)
class TermToPolynomialVisitor(TermVisitor[IntPolynomial]):
    @override
    def visit_variable(self, term: Variable) -> IntPolynomial:
        mon = Monomial.from_indeterminate(term.identifier)
        return IntPolynomial.from_monomial(mon)

    @override
    def visit_function(self, term: FunctionApplication) -> IntPolynomial:
        match term.symbol.name:
            case '0':
                return zero

            case '1':
                return const

            case '-':
                value, = (self.visit(arg) for arg in term.arguments)
                return -value

            case '+':
                left, right = (self.visit(arg) for arg in term.arguments)
                return left + right

            case '⋅':
                left, right = (self.visit(arg) for arg in term.arguments)
                return left * right

            case _:
                raise UnrecognizedSymbolError(f'Unknown {term.symbol.get_kind_string()} symbol {term.symbol}')


# This is alg:logical_term_to_integer_polynomial in the monograph
def term_to_polynomial(term: Term) -> IntPolynomial:
    return TermToPolynomialVisitor().visit(term)
