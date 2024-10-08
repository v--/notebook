from textwrap import dedent

import pytest

from ....parsing.identifiers import LatinIdentifier
from ....parsing.parser import ParsingError
from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..formulas import EqualityFormula
from ..signature import EMPTY_SIGNATURE, FOLSignature
from ..terms import FunctionTerm, Variable
from ..variables import common as var
from .parser import parse_formula, parse_term


@pytest_parametrize_kwargs(
    dict(
        term='x',
        expected=Variable(LatinIdentifier('x'))
    ),
    dict(
        term='y',
        expected=Variable(LatinIdentifier('y'))
    ),
    dict(
        term='y₁₂',
        expected=Variable(LatinIdentifier('y', index=12))
    )
)
def test_parsing_valid_variables(term: str, expected: Variable) -> None:
    assert parse_term(EMPTY_SIGNATURE, term) == expected


def test_parsing_invalid_variable_suffix() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(EMPTY_SIGNATURE, 'x₀₁')

    assert str(excinfo.value) == 'Nonzero natural numbers cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x₀₁
          │  ^^
        '''
    )


def test_parsing_accented_variable_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(EMPTY_SIGNATURE, 'ä')

    assert str(excinfo.value) == 'Unexpected symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ä
          │ ^
        '''
    )


def test_space_after_variable_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(EMPTY_SIGNATURE, 'x ')

    assert str(excinfo.value) == 'Finished parsing but there is still input left'
    assert excinfo.value.__notes__[0] == (
        '1 │ x \n'
        '  │  ^\n'
    )


@pytest_parametrize_kwargs(
    dict(
        term='f₀',
        expected=FunctionTerm('f₀', [])
    ),
    dict(
        term='f₁(x)',
        expected=FunctionTerm('f₁', [Variable(LatinIdentifier('x'))])
    ),
    dict(
        term='f₃(x, y, z)',
        expected=FunctionTerm('f₃', [Variable(LatinIdentifier(s)) for s in 'xyz'])
    ),
    dict(
        term='f₃(x,y,  z)',
        expected=FunctionTerm('f₃', [Variable(LatinIdentifier(s)) for s in 'xyz'])
    )
)
def test_parsing_valid_functions(term: str, expected: FunctionTerm, dummy_signature: FOLSignature) -> None:
    assert parse_term(dummy_signature, term) == expected


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
        parse_term(dummy_signature, 'f₀()')

    assert str(excinfo.value) == 'Avoid the argument list at all when zero arguments are expected'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₀()
          │ ^^^^
    ''')


def test_parsing_nonzero_arity_function_with_empty_arg_list(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'f₁()')

    assert str(excinfo.value) == 'Empty argument lists are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₁()
          │ ^^^^
    ''')


def test_parsing_function_with_only_open_paren(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'f₁(')

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₁(
          │ ^^^
    ''')


def test_parsing_function_with_unclosed_arg_list(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'f₂(x,y')

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₂(x,y
          │ ^^^^^^
    ''')


def test_parsing_function_with_missing_arg(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'f₂(x,)')

    assert str(excinfo.value) == 'Unexpected closing parenthesis for argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₂(x,)
          │ ^^^^^^
    ''')


def test_parsing_function_with_wrong_arity(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'f₂(x)')

    assert str(excinfo.value) == 'Expected 2 arguments for f₂ but got 1'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₂(x)
          │ ^^^^^
    ''')


@pytest_parametrize_kwargs(
    dict(
        term='(x = y)',
        expected=EqualityFormula(var.x, var.y)
    ),
    dict(
        term='(f₁(x) = f₂(y, z))',
        expected=EqualityFormula(
            FunctionTerm('f₁', [var.x]),
            FunctionTerm('f₂', [var.y, var.z]),
        )
    )
)
def test_parsing_valid_equalities(term: str, expected: EqualityFormula, dummy_signature: FOLSignature) -> None:
    assert parse_formula(dummy_signature, term) == expected


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
        parse_formula(dummy_signature, '(¬p₀ = y)')

    assert str(excinfo.value) == 'The left side of an equality formula must be a term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (¬p₀ = y)
          │  ^^^
    ''')


@pytest_parametrize_lists(
    formula=[
        '⊤',
        '⊥',
        '(x = y)',
        '∀x.p₁(y)',
        '(p₁(x) ∧ p₁(y))',
        '(¬p₁(z) ∧ ∀x.(q₂(z, x) → ¬r₂(y, x)))',
        '∀y.∃z.(¬p₁(z) ∧ ∀x.(q₂(z, x) → ¬r₂(y, x)))',
        '∀y.(∀z.(¬r₁(z) → ¬q₂(y, z)) → p₁(y))',
        '∀z.∃z.(¬r₁(y) ∧ ¬r₂(z, y))'
    ]
)
def test_rebuilding_formulas(formula: str, dummy_signature: FOLSignature) -> None:
    assert str(parse_formula(dummy_signature, formula)) == formula


def test_parsing_unclosed_conjunction_parentheses(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(p₀ ∧ q₀ ∧')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p₀ ∧ q₀ ∧
          │ ^^^^^^^^
    ''')


def test_parsing_unclosed_conjunction_parentheses_truncated(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(p₀ ∧ q₀')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p₀ ∧ q₀
          │ ^^^^^^^^
    ''')


def test_parsing_invalid_conjunction(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(p₀ ∧ )')

    assert str(excinfo.value) == 'Binary formulas must have a second subformula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p₀ ∧ )
          │ ^^^^^^^
    ''')


def test_parsing_conjunction_with_formulas_inside(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(x ∧ q₀)')

    assert str(excinfo.value) == 'The left side of a binary formula must be a formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x ∧ q₀)
          │  ^
    ''')


def test_complex_unbalanced_formula(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(∀x.(q₂(z, x) → ¬r₂(y, x) ∧ ¬p₁(z))')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (∀x.(q₂(z, x) → ¬r₂(y, x) ∧ ¬p₁(z))
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
        parse_formula(dummy_signature, '∀p₀.p₀')

    assert str(excinfo.value) == 'Expected a variable after the quantifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀p₀.p₀
          │ ^^^
    ''')


def test_quantifier_with_no_dot(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '∀xp₀')

    assert str(excinfo.value) == 'Expected dot after variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀xp₀
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



@pytest_parametrize_lists(
    formula=[
        '∀y.∃z.(¬p₁(z) ∧ ∀x.(q₂(z, x) → ¬r₂(y, x)))',
        '∀y.∃z.(¬p₁(z) ∧ ∀x.(q₂(z, x) → ¬r₂(y, x)))',
        '∀y₀.(∀z.(¬r₁(z) → ¬q₂(y₀, z)) → p₁(y₀))',
        '((∃x.p₁(x) ∧ ∃y.q₁(y)) ∨ (∃x.p₁(x) ∧ ∃y.q₁(y)))'
    ]
)
def test_reparsing_formulas(formula: str, dummy_signature: FOLSignature) -> None:
    assert str(parse_formula(dummy_signature, str(parse_formula(dummy_signature, formula)))) == formula

