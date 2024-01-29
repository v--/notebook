import pytest

from ..support.parsing import ParserError

from .terms import Variable, FunctionTerm
from .formulas import EqualityFormula
from .parser import parse_term, parse_formula


def test_parsing_variables_valid():
    assert parse_term('ξ') == Variable('ξ')
    assert parse_term('η') == Variable('η')
    assert parse_term('η12') == Variable('η12')


def test_parsing_variables_invalid():
    # Disallow leading zeros
    with pytest.raises(ParserError):
        parse_term('ξ0')

    # Allow only Greek letters for names
    assert not isinstance(parse_term('a'), Variable)

    # Not too Greek
    with pytest.raises(ParserError):
        parse_term('Εὐκλείδης')

    # And no trailing characters
    with pytest.raises(ParserError):
        parse_term('ξ ')


def test_parsing_functions_valid():
    assert parse_term('f') == FunctionTerm('f', [])
    assert parse_term('f13') == FunctionTerm('f13', [])
    assert parse_term('f(ξ)') == FunctionTerm('f', [Variable('ξ')])
    assert parse_term('f(ξ, η, ζ)') == FunctionTerm('f', [Variable('ξ'), Variable('η'), Variable('ζ')])
    assert parse_term('f(ξ,η,  ζ)') == FunctionTerm('f', [Variable('ξ'), Variable('η'), Variable('ζ')])


def test_parsing_functions_invalid():
    # Disallow leading zeros
    with pytest.raises(ParserError):
        parse_term('f0')

    # Only allow the letters from a to z and from α to ω
    with pytest.raises(ParserError):
        parse_term('ö')

    # Disallow empty argument list
    with pytest.raises(ParserError):
        parse_term('f()')

    # Validate closing parentheses
    with pytest.raises(ParserError):
        parse_term('f(')

    with pytest.raises(ParserError):
        parse_term('f(a,b')


def test_parsing_equalities_valid():
    assert parse_formula('(ξ = η)') == EqualityFormula(Variable('ξ'), Variable('η'))
    assert parse_formula('(f(ξ) = g(η, ζ))') == EqualityFormula(FunctionTerm('f', [Variable('ξ')]), FunctionTerm('g', [Variable('η'), Variable('ζ')]))


def test_parsing_equalities_invalid():
    # Disallow obviously invalid expressions
    with pytest.raises(ParserError):
        parse_formula('(ξ = )')

    # Parentheses must be closed
    with pytest.raises(ParserError):
        parse_formula('(ξ = η')

    # The left side of an equality formula must be a term
    with pytest.raises(ParserError):
        parse_formula('(¬p(ξ) = η)')


def test_parsing_formulas_valid():
    def is_formula_rebuilt(string: str):
        assert str(parse_formula(string)) == string

    is_formula_rebuilt('⊤')
    is_formula_rebuilt('⊥')
    is_formula_rebuilt('(ξ = η)')
    is_formula_rebuilt('∀ξ.p(η)')
    is_formula_rebuilt('(p(ξ) ∧ p(η))')
    is_formula_rebuilt('(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η.(∀ζ.(¬r(ζ) → ¬q(η, ζ)) → p(η))')
    is_formula_rebuilt('∀ζ.∃ζ.(¬r(η) ∧ ¬r(ζ, η))')


def test_parsing_formulas_invalid():
    # Parentheses must be closed
    with pytest.raises(ParserError):
        parse_formula('(p')

    with pytest.raises(ParserError):
        parse_formula('(p ∧')

    with pytest.raises(ParserError):
        parse_formula('(p ∧ q')

    with pytest.raises(ParserError):
        parse_formula('(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ))')

    # No trailing characters
    with pytest.raises(ParserError):
        parse_term('p ')

    # No incomplete quantifier formulas
    with pytest.raises(ParserError):
        parse_term('∀')

    with pytest.raises(ParserError):
        parse_term('∀ξ')

    with pytest.raises(ParserError):
        parse_term('∀ξ.')

    # No invalid variables
    with pytest.raises(ParserError):
        parse_term('∀x')


def test_reparsing_formulas():
    def is_formula_rebuilt(string: str):
        assert str(parse_formula(str(parse_formula(string)))) == string

    is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η1.(∀ζ.(¬r(ζ) → ¬q(η1, ζ)) → p(η1))')
    is_formula_rebuilt('((∃ξ.p(ξ) ∧ ∃η.q(η)) ∨ (∃ξ.p(ξ) ∧ ∃η.q(η)))')
