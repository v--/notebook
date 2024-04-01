from textwrap import dedent

import pytest

from ....parsing.parser import ParsingError
from ..formulas import EqualityFormula
from ..terms import FunctionTerm, Variable
from .parser import parse_formula, parse_term


def test_parsing_valid_variables():
    assert parse_term('ξ') == Variable('ξ')
    assert parse_term('η') == Variable('η')
    assert parse_term('η₁₂') == Variable('η₁₂')


def test_parsing_invalid_variable_suffix():
    with pytest.raises(ParsingError) as excinfo:
        parse_term('ξ₀₁')

    assert str(excinfo.value) == 'Nonzero natural numbers cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ξ₀₁
          │  ^^
        '''
    )


def test_parsing_latin_variable_name():
    # Allow only Greek letters for names
    assert not isinstance(parse_term('a'), Variable)


def test_parsing_accented_greek_variable_name():
    with pytest.raises(ParsingError) as excinfo:
        parse_term('Εὐκλείδης')

    assert str(excinfo.value) == 'Unexpected symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ Εὐκλείδης
          │  ^
        '''
    )


def test_space_after_variable_name():
    with pytest.raises(ParsingError) as excinfo:
        parse_term('ξ ')

    assert str(excinfo.value) == 'Finished parsing but there is still input left'
    assert excinfo.value.__notes__[0] == (
        '1 │ ξ \n'
        '  │  ^\n'
    )


def test_parsing_valid_functions():
    assert parse_term('f') == FunctionTerm('f', [])
    assert parse_term('f₁₂') == FunctionTerm('f₁₂', [])
    assert parse_term('f(ξ)') == FunctionTerm('f', [Variable('ξ')])
    assert parse_term('f(ξ, η, ζ)') == FunctionTerm('f', [Variable('ξ'), Variable('η'), Variable('ζ')])
    assert parse_term('f(ξ,η,  ζ)') == FunctionTerm('f', [Variable('ξ'), Variable('η'), Variable('ζ')])


def test_parsing_invalid_function_suffix():
    with pytest.raises(ParsingError) as excinfo:
        parse_term('f₀₀')

    assert str(excinfo.value) == 'Nonzero natural numbers cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₀₀
          │  ^^
    ''')


def test_parsing_function_with_empty_arg_list():
    with pytest.raises(ParsingError) as excinfo:
        parse_term('f()')

    assert str(excinfo.value) == 'Empty argument list disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f()
          │  ^^
    ''')


def test_parsing_function_with_only_open_paren():
    with pytest.raises(ParsingError) as excinfo:
        parse_term('f(')

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f(
          │  ^
    ''')


def test_parsing_function_with_unclosed_arg_list():
    with pytest.raises(ParsingError) as excinfo:
        parse_term('f(a,b')

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f(a,b
          │  ^^^^
    ''')


def test_parsing_valid_equalities():
    assert parse_formula('(ξ = η)') == EqualityFormula(Variable('ξ'), Variable('η'))
    assert parse_formula('(f(ξ) = g(η, ζ))') == EqualityFormula(FunctionTerm('f', [Variable('ξ')]), FunctionTerm('g', [Variable('η'), Variable('ζ')]))


def test_parsing_unclosed_equality_parentheses():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(ξ = η =')

    assert str(excinfo.value) == 'Unclosed parentheses for equality formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ξ = η =
          │ ^^^^^^
    ''')


def test_parsing_unclosed_equality_parentheses_truncated():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(ξ = η')

    assert str(excinfo.value) == 'Unclosed parentheses for equality formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ξ = η
          │ ^^^^^^
    ''')


def test_parsing_invalid_equality():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(ξ = )')

    assert str(excinfo.value) == 'Equality formulas must have a second term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ξ = )
          │ ^^^^^^
    ''')


def test_parsing_equality_with_formulas_inside():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(¬p = η)')

    assert str(excinfo.value) == 'The left side of an equality formula must be a term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (¬p = η)
          │  ^^
    ''')


def test_parsing_valid_formulas():
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


def test_parsing_unclosed_conjunction_parentheses():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(p ∧ q ∧')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ q ∧
          │ ^^^^^^
    ''')


def test_parsing_unclosed_conjunction_parentheses_truncated():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(p ∧ q')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ q
          │ ^^^^^^
    ''')


def test_parsing_invalid_conjunction():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(p ∧ )')

    assert str(excinfo.value) == 'Binary formulas must have a second subformula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ )
          │ ^^^^^^
    ''')


def test_parsing_conjunction_with_formulas_inside():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(ξ ∧ q)')

    assert str(excinfo.value) == 'The left side of a binary formula must be a formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ξ ∧ q)
          │  ^
    ''')


def test_complex_unbalanced_formula():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('(∀ξ.(q(ζ, ξ) → ¬r(η, ξ) ∧ ¬p(ζ))')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (∀ξ.(q(ζ, ξ) → ¬r(η, ξ) ∧ ¬p(ζ))
          │     ^^^^^^^^^^^^^^^^^^^
    ''')


def test_lone_quantifier():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('∀')

    assert str(excinfo.value) == 'Expected a variable after the quantifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀
          │ ^
    ''')


def test_quantifier_with_latin_variable():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('∀x.p')

    assert str(excinfo.value) == 'Expected a variable after the quantifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀x.p
          │ ^^
    ''')


def test_quantifier_with_no_dot():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('∀ξp')

    assert str(excinfo.value) == 'Expected dot after variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀ξp
          │ ^^^
    ''')


def test_quantifier_with_no_subformula():
    with pytest.raises(ParsingError) as excinfo:
        parse_formula('∀ξ.')

    assert str(excinfo.value) == 'Unexpected end of input'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀ξ.
          │   ^
    ''')


def test_reparsing_formulas():
    def is_formula_rebuilt(string: str):
        assert str(parse_formula(str(parse_formula(string)))) == string

    is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η.∃ζ.(¬p(ζ) ∧ ∀ξ.(q(ζ, ξ) → ¬r(η, ξ)))')
    is_formula_rebuilt('∀η₀.(∀ζ.(¬r(ζ) → ¬q(η₀, ζ)) → p(η₀))')
    is_formula_rebuilt('((∃ξ.p(ξ) ∧ ∃η.q(η)) ∨ (∃ξ.p(ξ) ∧ ∃η.q(η)))')
