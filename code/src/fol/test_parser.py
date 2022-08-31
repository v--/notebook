import pytest
from parsimonious.exceptions import ParseError

from .types import Variable, FunctionTerm, EqualityFormula
from .parser import parse, parse_formula


def test_parsing_variables():
    assert parse('ξ', rule='variable') == Variable('ξ')
    assert parse('η', rule='variable') == Variable('η')
    assert parse('η12', rule='variable') == Variable('η12')
    assert parse('Εὐκλείδης', rule='variable') == Variable('Εὐκλείδης')

    # Only Greek letters
    with pytest.raises(ParseError):
        parse('a', rule='variable')

    # Only positive integers
    with pytest.raises(ParseError):
        parse('η0', rule='variable')


def test_parsing_functions():
    assert parse('f(ξ)', rule='function') == FunctionTerm('f', [Variable('ξ')])
    assert parse('f(ξ, η, ζ)', rule='function') == FunctionTerm('f', [Variable('ξ'), Variable('η'), Variable('ζ')])
    assert parse('f(ξ,η,  ζ)', rule='function') == FunctionTerm('f', [Variable('ξ'), Variable('η'), Variable('ζ')])


def test_parsing_equalities():
    assert parse('(ξ = η)', rule='equality') == EqualityFormula(Variable('ξ'), Variable('η'))
    assert parse('(f(ξ) = g(η, ζ))', rule='equality') == EqualityFormula(FunctionTerm('f', [Variable('ξ')]), FunctionTerm('g', [Variable('η'), Variable('ζ')]))


def test_parsing_formulas():
    def is_formula_rebuilt(string: str):
        assert str(parse_formula(string)) == string

    is_formula_rebuilt('(ξ = η)')
    is_formula_rebuilt('∀ξ.p(η)')
    is_formula_rebuilt('(p(ξ) ∧ p(η))')
    is_formula_rebuilt('(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η.(∀ζ.(¬r(ζ) → ¬q(η, ζ)) → p(η))')
    is_formula_rebuilt('∀ζ.∃ζ.(¬r(η) ∧ ¬r(ζ, η))')


def test_reparsing_formulas():
    def is_formula_rebuilt(string: str):
        assert str(parse_formula(str(parse_formula(string)))) == string

    is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η1.(∀ζ.(¬r(ζ) → ¬q(η1, ζ)) → p(η1))')
    is_formula_rebuilt('((∃ξ.p(ξ) ∧ ∃η.q(η)) ∨ (∃ξ.p(ξ) ∧ ∃η.q(η)))')
