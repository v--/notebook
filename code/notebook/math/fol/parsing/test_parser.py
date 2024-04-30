from textwrap import dedent

import pytest

from ....parsing.parser import ParsingError
from ..formulas import EqualityFormula
from ..signature import FOLSignature
from ..terms import FunctionTerm, Variable
from .parser import parse_formula, parse_propositional_formula, parse_term


def test_parsing_valid_variables(empty_signature: FOLSignature) -> None:
    assert parse_term(empty_signature, 'ξ') == Variable('ξ')
    assert parse_term(empty_signature, 'η') == Variable('η')
    assert parse_term(empty_signature, 'η₁₂') == Variable('η₁₂')


def test_parsing_invalid_variable_suffix(empty_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(empty_signature, 'ξ₀₁')

    assert str(excinfo.value) == 'Nonzero natural numbers cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ξ₀₁
          │  ^^
        '''
    )


def test_parsing_accented_greek_variable_name(empty_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(empty_signature, 'Εὐκλείδης')

    assert str(excinfo.value) == 'Unexpected symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ Εὐκλείδης
          │  ^
        '''
    )


def test_space_after_variable_name(empty_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(empty_signature, 'ξ ')

    assert str(excinfo.value) == 'Finished parsing but there is still input left'
    assert excinfo.value.__notes__[0] == (
        '1 │ ξ \n'
        '  │  ^\n'
    )


def test_parsing_valid_functions(dummy_signature: FOLSignature) -> None:
    assert parse_term(dummy_signature, 'f₀') == FunctionTerm('f₀', [])
    assert parse_term(dummy_signature, 'f₁(ξ)') == FunctionTerm('f₁', [Variable('ξ')])
    assert parse_term(dummy_signature, 'f₃(ξ, η, ζ)') == FunctionTerm('f₃', [Variable('ξ'), Variable('η'), Variable('ζ')])
    assert parse_term(dummy_signature, 'f₃(ξ,η,  ζ)') == FunctionTerm('f₃', [Variable('ξ'), Variable('η'), Variable('ζ')])


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
        parse_term(dummy_signature, 'f₂(ξ,η')

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₂(ξ,η
          │ ^^^^^^
    ''')


def test_parsing_function_with_missing_arg(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'f₂(ξ,)')

    assert str(excinfo.value) == 'Unexpected closing parenthesis for argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₂(ξ,)
          │ ^^^^^^
    ''')


def test_parsing_function_with_wrong_arity(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(dummy_signature, 'f₂(ξ)')

    assert str(excinfo.value) == 'Expected 2 arguments for f₂ but got 1'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f₂(ξ)
          │ ^^^^^
    ''')


def test_parsing_valid_equalities(dummy_signature: FOLSignature) -> None:
    assert parse_formula(dummy_signature, '(ξ = η)') == EqualityFormula(Variable('ξ'), Variable('η'))
    assert parse_formula(dummy_signature, '(f₁(ξ) = f₂(η, ζ))') == EqualityFormula(FunctionTerm('f₁', [Variable('ξ')]), FunctionTerm('f₂', [Variable('η'), Variable('ζ')]))


def test_parsing_unclosed_equality_parentheses(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(ξ = η =')

    assert str(excinfo.value) == 'Unclosed parentheses for equality formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ξ = η =
          │ ^^^^^^
    ''')


def test_parsing_unclosed_equality_parentheses_truncated(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(ξ = η')

    assert str(excinfo.value) == 'Unclosed parentheses for equality formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ξ = η
          │ ^^^^^^
    ''')


def test_parsing_invalid_equality(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(ξ = )')

    assert str(excinfo.value) == 'Equality formulas must have a second term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ξ = )
          │ ^^^^^^
    ''')


def test_parsing_equality_with_formulas_inside() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_propositional_formula('(¬p = η)')

    assert str(excinfo.value) == 'The left side of an equality formula must be a term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (¬p = η)
          │  ^^
    ''')


def test_parsing_valid_formulas(dummy_signature: FOLSignature) -> None:
    def is_formula_rebuilt(string: str) -> None:
        assert str(parse_formula(dummy_signature, string)) == string

    is_formula_rebuilt('⊤')
    is_formula_rebuilt('⊥')
    is_formula_rebuilt('(ξ = η)')
    is_formula_rebuilt('∀ξ.p₁(η)')
    is_formula_rebuilt('(p₁(ξ) ∧ p₁(η))')
    is_formula_rebuilt('(¬p₁(ζ) ∧ ∀ξ.(q₂(ζ, ξ) → ¬r₂(η, ξ)))')
    is_formula_rebuilt('∀η.∃ζ.(¬p₁(ζ) ∧ ∀ξ.(q₂(ζ, ξ) → ¬r₂(η, ξ)))')
    is_formula_rebuilt('∀η.(∀ζ.(¬r₁(ζ) → ¬q₂(η, ζ)) → p₁(η))')
    is_formula_rebuilt('∀ζ.∃ζ.(¬r₁(η) ∧ ¬r₂(ζ, η))')


def test_parsing_unclosed_conjunction_parentheses() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_propositional_formula('(p ∧ q ∧')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ q ∧
          │ ^^^^^^
    ''')


def test_parsing_unclosed_conjunction_parentheses_truncated() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_propositional_formula('(p ∧ q')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ q
          │ ^^^^^^
    ''')


def test_parsing_invalid_conjunction() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_propositional_formula('(p ∧ )')

    assert str(excinfo.value) == 'Binary formulas must have a second subformula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ )
          │ ^^^^^^
    ''')


def test_parsing_conjunction_with_formulas_inside() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_propositional_formula('(ξ ∧ q)')

    assert str(excinfo.value) == 'The left side of a binary formula must be a formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ξ ∧ q)
          │  ^
    ''')


def test_complex_unbalanced_formula(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '(∀ξ.(q₂(ζ, ξ) → ¬r₂(η, ξ) ∧ ¬p₁(ζ))')

    assert str(excinfo.value) == 'Unclosed parentheses for binary formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (∀ξ.(q₂(ζ, ξ) → ¬r₂(η, ξ) ∧ ¬p₁(ζ))
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


def test_quantifier_with_latin_variable(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '∀p₀.p₀')

    assert str(excinfo.value) == 'Expected a variable after the quantifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀p₀.p₀
          │ ^^^
    ''')


def test_quantifier_with_no_dot(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '∀ξp₀')

    assert str(excinfo.value) == 'Expected dot after variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀ξp₀
          │ ^^^^
    ''')


def test_quantifier_with_no_subformula(dummy_signature: FOLSignature) -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_formula(dummy_signature, '∀ξ.')

    assert str(excinfo.value) == 'Unexpected end of input'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀ξ.
          │   ^
    ''')


def test_reparsing_formulas(dummy_signature: FOLSignature) -> None:
    def is_formula_rebuilt(string: str) -> None:
        assert str(parse_formula(dummy_signature, str(parse_formula(dummy_signature, string)))) == string

    is_formula_rebuilt('∀η.∃ζ.(¬p₁(ζ) ∧ ∀ξ.(q₂(ζ, ξ) → ¬r₂(η, ξ)))')
    is_formula_rebuilt('∀η.∃ζ.(¬p₁(ζ) ∧ ∀ξ.(q₂(ζ, ξ) → ¬r₂(η, ξ)))')
    is_formula_rebuilt('∀η₀.(∀ζ.(¬r₁(ζ) → ¬q₂(η₀, ζ)) → p₁(η₀))')
    is_formula_rebuilt('((∃ξ.p₁(ξ) ∧ ∃η.q₁(η)) ∨ (∃ξ.p₁(ξ) ∧ ∃η.q₁(η)))')
