from textwrap import dedent

import pytest

from ....parsing.identifiers import LatinIdentifier
from ....parsing.parser import ParsingError
from ..formulas import EqualityFormula
from ..signature import FOLSignature
from ..terms import FunctionTerm, Variable
from .parser import parse_formula, parse_term


def test_parsing_valid_variables(empty_signature: FOLSignature) -> None:
    assert parse_term(empty_signature, 'x') == Variable(LatinIdentifier('x'))
    assert parse_term(empty_signature, 'y') == Variable(LatinIdentifier('y'))
    assert parse_term(empty_signature, 'y₁₂') == Variable(LatinIdentifier('y', index=12))


def test_parsing_invalid_variable_suffix(empty_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(empty_signature, 'x₀₁')

    assert str(excinfo.value) == 'Nonzero natural numbers cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x₀₁
          │  ^^
        '''
    )


def test_parsing_accented_variable_name(empty_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(empty_signature, 'ä')

    assert str(excinfo.value) == 'Unexpected symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ä
          │ ^
        '''
    )


def test_space_after_variable_name(empty_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(empty_signature, 'x ')

    assert str(excinfo.value) == 'Finished parsing but there is still input left'
    assert excinfo.value.__notes__[0] == (
        '1 │ x \n'
        '  │  ^\n'
    )


def test_parsing_valid_functions(dummy_signature: FOLSignature) -> None:
    x = parse_term(dummy_signature, 'x')
    y = parse_term(dummy_signature, 'y')
    z = parse_term(dummy_signature, 'z')

    assert parse_term(dummy_signature, 'F₀') == FunctionTerm('F₀', [])
    assert parse_term(dummy_signature, 'F₁(x)') == FunctionTerm('F₁', [x])
    assert parse_term(dummy_signature, 'F₃(x, y, z)') == FunctionTerm('F₃', [x, y, z])
    assert parse_term(dummy_signature, 'F₃(x,y,  z)') == FunctionTerm('F₃', [x, y, z])


def test_parsing_functions_with_unrecognized_names(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'F')

    assert str(excinfo.value) == 'Unexpected symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ F
          │ ^
    ''')


def test_parsing_zero_arity_function_with_empty_arg_list(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'F₀()')

    assert str(excinfo.value) == 'Avoid the argument list at all when zero arguments are expected'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ F₀()
          │ ^^^^
    ''')


def test_parsing_nonzero_arity_function_with_empty_arg_list(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'F₁()')

    assert str(excinfo.value) == 'Empty argument lists are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ F₁()
          │ ^^^^
    ''')


def test_parsing_function_with_only_open_paren(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'F₁(')

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ F₁(
          │ ^^^
    ''')


def test_parsing_function_with_unclosed_arg_list(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'F₂(x,y')

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ F₂(x,y
          │ ^^^^^^
    ''')


def test_parsing_function_with_missing_arg(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'F₂(x,)')

    assert str(excinfo.value) == 'Unexpected closing parenthesis for argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ F₂(x,)
          │ ^^^^^^
    ''')


def test_parsing_function_with_wrong_arity(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'F₂(x)')

    assert str(excinfo.value) == 'Expected 2 arguments for F₂ but got 1'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ F₂(x)
          │ ^^^^^
    ''')


def test_parsing_valid_equalities(dummy_signature: FOLSignature) -> None:
    x = parse_term(dummy_signature, 'x')
    y = parse_term(dummy_signature, 'y')
    z = parse_term(dummy_signature, 'z')

    assert parse_formula(dummy_signature, '(x = y)') == EqualityFormula(x, y)
    assert parse_formula(dummy_signature, '(F₁(x) = F₂(y, z))') == EqualityFormula(FunctionTerm('F₁', [x]), FunctionTerm('F₂', [y, z]))


def test_parsing_unclosed_equality_parentheses(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(x = y =')

    assert str(excinfo.value) == 'Unclosed parentheses for equality formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x = y =
          │ ^^^^^^
    ''')


def test_parsing_unclosed_equality_parentheses_truncated(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(x = y')

    assert str(excinfo.value) == 'Unclosed parentheses for equality formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x = y
          │ ^^^^^^
    ''')


def test_parsing_invalid_equality(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(x = )')

    assert str(excinfo.value) == 'Equality formulas must have a second term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x = )
          │ ^^^^^^
    ''')


def test_parsing_equality_with_formulas_inside(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(¬P₀ = y)')

    assert str(excinfo.value) == 'The left side of an equality formula must be a term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (¬P₀ = y)
          │  ^^^
    ''')


def test_parsing_valid_formulas(dummy_signature: FOLSignature) -> None:
    def is_formula_rebuilt(string: str) -> None:
        assert str(parse_formula(dummy_signature, string)) == string

    is_formula_rebuilt('⊤')
    is_formula_rebuilt('⊥')
    is_formula_rebuilt('(x = y)')
    is_formula_rebuilt('∀x.P₁(y)')
    is_formula_rebuilt('(P₁(x) ∧ P₁(y))')
    is_formula_rebuilt('(¬P₁(z) ∧ ∀x.(Q₂(z, x) → ¬R₂(y, x)))')
    is_formula_rebuilt('∀y.∃z.(¬P₁(z) ∧ ∀x.(Q₂(z, x) → ¬R₂(y, x)))')
    is_formula_rebuilt('∀y.(∀z.(¬R₁(z) → ¬Q₂(y, z)) → P₁(y))')
    is_formula_rebuilt('∀z.∃z.(¬R₁(y) ∧ ¬R₂(z, y))')


def test_parsing_unclosed_conjunction_parentheses(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(P₀ ∧ Q₀ ∧')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (P₀ ∧ Q₀ ∧
          │ ^^^^^^^^
    ''')


def test_parsing_unclosed_conjunction_parentheses_truncated(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(P₀ ∧ Q₀')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (P₀ ∧ Q₀
          │ ^^^^^^^^
    ''')


def test_parsing_invalid_conjunction(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(P₀ ∧ )')

    assert str(excinfo.value) == 'Binary formulas must have a second subformula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (P₀ ∧ )
          │ ^^^^^^^
    ''')


def test_parsing_conjunction_with_formulas_inside(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(x ∧ Q₀)')

    assert str(excinfo.value) == 'The left side of a binary formula must be a formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x ∧ Q₀)
          │  ^
    ''')


def test_complex_unbalanced_formula(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(∀x.(Q₂(z, x) → ¬R₂(y, x) ∧ ¬P₁(z))')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (∀x.(Q₂(z, x) → ¬R₂(y, x) ∧ ¬P₁(z))
          │     ^^^^^^^^^^^^^^^^^^^^^
    ''')


def test_lone_quantifier(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '∀')

    assert str(excinfo.value) == 'Expected a variable after the quantifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀
          │ ^
    ''')


def test_quantifier_with_invalid_variable(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '∀P₀.P₀')

    assert str(excinfo.value) == 'Expected a variable after the quantifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀P₀.P₀
          │ ^^^
    ''')


def test_quantifier_with_no_dot(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '∀xP₀')

    assert str(excinfo.value) == 'Expected dot after variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀xP₀
          │ ^^^^
    ''')


def test_quantifier_with_no_subformula(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '∀x.')

    assert str(excinfo.value) == 'Unexpected end of input'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀x.
          │   ^
    ''')


def test_reparsing_formulas(dummy_signature: FOLSignature) -> None:
    def is_formula_rebuilt(string: str) -> None:
        assert str(parse_formula(dummy_signature, str(parse_formula(dummy_signature, string)))) == string

    is_formula_rebuilt('∀y.∃z.(¬P₁(z) ∧ ∀x.(Q₂(z, x) → ¬R₂(y, x)))')
    is_formula_rebuilt('∀y.∃z.(¬P₁(z) ∧ ∀x.(Q₂(z, x) → ¬R₂(y, x)))')
    is_formula_rebuilt('∀y₀.(∀z.(¬R₁(z) → ¬Q₂(y₀, z)) → P₁(y₀))')
    is_formula_rebuilt('((∃x.P₁(x) ∧ ∃y.Q₁(y)) ∨ (∃x.P₁(x) ∧ ∃y.Q₁(y)))')
