import pytest


from ..support.parsing import ParserError
from ..grammars.grammar import NonTerminal

from .types import Variable, FunctionTerm, EqualityFormula
from .parser import parse, parse_formula


def test_parsing_numbers():
    assert parse('0', rule=NonTerminal('natural_number')) == '0'
    assert parse('9', rule=NonTerminal('natural_number')) == '9'
    assert parse('10', rule=NonTerminal('natural_number')) == '10'
    assert parse('169', rule=NonTerminal('natural_number')) == '169'

    with pytest.raises(ParserError):
        parse('01', rule=NonTerminal('natural_number'))

    with pytest.raises(ParserError):
        parse('00', rule=NonTerminal('natural_number'))


def test_parsing_variables():
    assert parse('ξ', rule=NonTerminal('variable')) == Variable('ξ')
    assert parse('η', rule=NonTerminal('variable')) == Variable('η')
    assert parse('η12', rule=NonTerminal('variable')) == Variable('η12')

    # Allow only Greek letters for names
    with pytest.raises(ParserError):
        parse('a', rule=NonTerminal('variable'))

    # # Not too Greek
    # with pytest.raises(ParserError):
    #     parse('Εὐκλείδης', rule=NonTerminal('variable'))


def xtest_parsing_spaces():
    assert parse(' ', rule=NonTerminal('opt_space')) == ' '
    assert parse('  ', rule=NonTerminal('opt_space')) == '  '


def test_parsing_functions():
    assert parse('f(ξ)', rule=NonTerminal('function')) == FunctionTerm('f', [Variable('ξ')])
    assert parse('f(ξ,η,ζ)', rule=NonTerminal('function')) == FunctionTerm('f', [Variable('ξ'), Variable('η'), Variable('ζ')])
    # assert parse('f(ξ,η,  ζ)', rule=NonTerminal('function')) == FunctionTerm('f', [Variable('ξ'), Variable('η'), Variable('ζ')])


def xtest_parsing_equalities():
    assert parse('(ξ = η)', rule=NonTerminal('equality')) == EqualityFormula(Variable('ξ'), Variable('η'))
    assert parse('(f(ξ) = g(η, ζ))', rule=NonTerminal('equality')) == EqualityFormula(FunctionTerm('f', [Variable('ξ')]), FunctionTerm('g', [Variable('η'), Variable('ζ')]))


def xtest_parsing_formulas():
    def is_formula_rebuilt(string: str):
        assert str(parse_formula(string)) == string

    # is_formula_rebuilt('(ξ = η)')
    # is_formula_rebuilt('∀ξ.p(η)')
    # is_formula_rebuilt('(p(ξ) ∧ p(η))')
    is_formula_rebuilt('(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    # is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    # is_formula_rebuilt('∀η.(∀ζ.(¬r(ζ) → ¬q(η, ζ)) → p(η))')
    # is_formula_rebuilt('∀ζ.∃ζ.(¬r(η) ∧ ¬r(ζ, η))')


def xtest_reparsing_formulas():
    def is_formula_rebuilt(string: str):
        assert str(parse_formula(string)) == string

    # is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    # is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    # is_formula_rebuilt('∀η1.(∀ζ.(¬r(ζ) → ¬q(η1, ζ)) → p(η1))')
    # is_formula_rebuilt('((∃ξ.p(ξ) ∧ ∃η.q(η)) ∨ (∃ξ.p(ξ) ∧ ∃η.q(η)))')
