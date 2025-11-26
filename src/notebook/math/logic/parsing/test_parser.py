from collections.abc import Sequence
from textwrap import dedent

import pytest

from ....parsing import LatinIdentifier, ParserError, TokenizerError
from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..formulas import EqualityFormula
from ..signature import EMPTY_SIGNATURE, FormalLogicSignature
from ..terms import EigenvariableSchemaSubstitutionSpec, FunctionApplication, Variable, VariablePlaceholder
from .parser import (
    parse_formula,
    parse_formula_schema,
    parse_formula_schema_with_substitution,
    parse_natural_deduction_rule,
    parse_propositional_formula,
    parse_term,
    parse_term_schema_substitution_spec,
    parse_variable,
)


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
    assert parse_variable(term) == expected


@pytest_parametrize_kwargs(
    dict(
        term='f⁰',
        name='f⁰',
        arguments=[]
    ),
    dict(
        term='f¹(x)',
        name='f¹',
        arguments=['x']
    ),
    dict(
        term='f³(x, y, z)',
        name='f³',
        arguments=list('xyz')
    ),
    dict(
        term='f³(x,y,  z)',
        name='f³',
        arguments=list('xyz')
    )
)
def test_parsing_valid_functions(term: str, name: str, arguments: Sequence[str], dummy_signature: FormalLogicSignature) -> None:
    expected = FunctionApplication(dummy_signature[name], [parse_term(arg, dummy_signature) for arg in arguments])
    assert parse_term(term, dummy_signature) == expected


def test_parsing_functions_with_unrecognized_names() -> None:
    with pytest.raises(TokenizerError) as excinfo:
        parse_term('Ḟ')

    assert str(excinfo.value) == 'Unexpected symbol'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ Ḟ
          │ ^
    ''')


def test_parsing_predicate_as_term(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('p⁰', dummy_signature)

    assert str(excinfo.value) == 'Encountered a formula where a term was expected'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ p⁰
          │ ^^
    ''')


def test_parsing_nonzero_arity_function_with_empty_arg_list(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('f¹()', dummy_signature)

    assert str(excinfo.value) == 'Empty argument lists are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f¹()
          │ ^^^^
    ''')


def test_parsing_function_with_only_open_paren(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('f¹(', dummy_signature)

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f¹(
          │ ^^^
    ''')


def test_parsing_function_with_unclosed_arg_list(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('f²(x,y', dummy_signature)

    assert str(excinfo.value) == 'Unclosed argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f²(x,y
          │ ^^^^^^
    ''')


def test_parsing_function_with_missing_arg(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('f²(x,)', dummy_signature)

    assert str(excinfo.value) == 'Unexpected closing parenthesis for argument list'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f²(x,)
          │ ^^^^^^
    ''')


def test_parsing_function_with_wrong_arity(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('f²(x)', dummy_signature)

    assert str(excinfo.value) == 'Expected 2 arguments for the function f², but got 1'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f²(x)
          │ ^^^^^
    ''')


def test_parsing_parenthesized_expression_without_symbol(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('(x', dummy_signature)

    assert str(excinfo.value) == 'Parenthesized expression must have a propositional connective, infix proper symbol or equality after the first subexpression'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x
          │ ^^
    ''')


def test_parsing_unrecognized_infix_symbol(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('(x ( y)', dummy_signature)

    assert str(excinfo.value) == "The symbol '(' is not an infix operator"
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x ( y)
          │    ^
    ''')


def test_parsing_infix_function(dummy_signature: FormalLogicSignature) -> None:
    string = '(x ∘ y)'
    term = parse_term(string, dummy_signature)
    assert str(term) == string


def test_parsing_nested_infix_functions(dummy_signature: FormalLogicSignature) -> None:
    string = '((x ∘ y) ∘ z)'
    term = parse_term(string, dummy_signature)
    assert str(term) == string


def test_parsing_infix_function_without_second_term(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('(x ∘', dummy_signature)

    assert str(excinfo.value) == 'Infix applications must have a second term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x ∘
          │ ^^^^
    ''')

def test_parsing_infix_function_without_closing_parens(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('(x ≠ y', dummy_signature)

    assert str(excinfo.value) == 'Infix applications must have a closing parenthesis'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x ≠ y
          │ ^^^^^^
    ''')

def test_parsing_infix_function_with_non_infix_notation(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('∘(x, y)', dummy_signature)

    assert str(excinfo.value) == 'Expected a prefix proper symbol, but got ∘'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∘(x, y)
          │ ^
    ''')


def test_parsing_non_infix_function_with_infix_notation(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('(x f³ y)', dummy_signature)

    assert str(excinfo.value) == 'Expected an infix proper symbol, but got f³'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x f³ y)
          │    ^^
    ''')


def test_parsing_infix_predicate(dummy_signature: FormalLogicSignature) -> None:
    string = '(x ≠ y)'
    term = parse_formula(string, dummy_signature)
    assert str(term) == string


def test_parsing_infix_predicate_without_second_term(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(x ≠', dummy_signature)

    assert str(excinfo.value) == 'Infix applications must have a second term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x ≠
          │ ^^^^
    ''')

def test_parsing_infix_predicate_without_closing_parens(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(x ≠ y', dummy_signature)

    assert str(excinfo.value) == 'Infix applications must have a closing parenthesis'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x ≠ y
          │ ^^^^^^
    ''')

def test_parsing_infix_predicate_with_non_infix_notation(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('≠(x, y)', dummy_signature)

    assert str(excinfo.value) == 'Expected a prefix proper symbol, but got ≠'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ≠(x, y)
          │ ^
    ''')


def test_parsing_non_infix_predicate_with_infix_notation(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(x p³ y)', dummy_signature)

    assert str(excinfo.value) == 'Expected an infix proper symbol, but got p³'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x p³ y)
          │    ^^
    ''')



@pytest_parametrize_lists(
    formula=[
        'p²((x ∘ y), z)',
        '((x ∘ y) ≠ f³(x, y, z))',
    ]
)
def test_mixing_prefix_and_infix_notation(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(parse_formula(formula, dummy_signature)) == formula


@pytest_parametrize_lists(
    term=[
        'fᶜ⁰',
        'fᶜ¹x',
        'fᶜ²xgᶜ⁰',
        'fᶜ²xgᶜ¹y',
    ]
)
def test_parsing_term_with_condensed_notation(term: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(parse_term(term, dummy_signature)) == term


def test_parsing_prefix_function_without_parentheses(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('f¹x', dummy_signature)

    assert str(excinfo.value) == 'Expected a parenthesized argument list for the function f¹'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f¹x
          │ ^^^
    ''')


def test_parsing_condensed_function_with_parentheses(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('fᶜ¹(', dummy_signature)

    assert str(excinfo.value) == 'Parentheses are disallowed for the symbol fᶜ¹ that uses condensed notation'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ fᶜ¹(
          │ ^^^^
    ''')


def test_parsing_condensed_function_with_missing_arguments(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('fᶜ¹', dummy_signature)

    assert str(excinfo.value) == 'Insufficient arguments for the symbol fᶜ¹ of arity 1'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ fᶜ¹
          │ ^^^
    ''')



@pytest_parametrize_kwargs(
    dict(
        left='x',
        right='x',
    ),
    dict(
        left='f¹(x)',
        right='f²(y, z)',
    )
)
def test_parsing_valid_equalities(left: str, right: str, dummy_signature: FormalLogicSignature) -> None:
    formula = f'({left} = {right})'
    expected = EqualityFormula(parse_term(left, dummy_signature), parse_term(right, dummy_signature))
    assert parse_formula(formula, dummy_signature) == expected


def test_parsing_unclosed_equality_parentheses(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(x = y =', dummy_signature)

    assert str(excinfo.value) == 'Equality formulas must have a closing parenthesis'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x = y =
          │ ^^^^^^^^
    ''')


def test_parsing_unclosed_equality_parentheses_truncated() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(x = y')

    assert str(excinfo.value) == 'Equality formulas must have a closing parenthesis'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x = y
          │ ^^^^^^
    ''')


def test_parsing_invalid_equality() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(x = )')

    assert str(excinfo.value) == 'Equality formulas must have a second term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x = )
          │ ^^^^^^
    ''')


def test_parsing_equality_with_formulas_inside(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(¬p⁰ = y)', dummy_signature)

    assert str(excinfo.value) == 'The first argument of an equality formula must be a term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (¬p⁰ = y)
          │  ^^^
    ''')


@pytest_parametrize_lists(
    formula=[
        '⊤',
        '⊥',
        '(x = y)',
        '∀x.p¹(y)',
        '(p¹(x) ∧ p¹(y))',
        '(¬p¹(z) ∧ ∀x.(q²(z, x) → ¬r²(y, x)))',
        '∀y.∃z.(¬p¹(z) ∧ ∀x.(q²(z, x) → ¬r²(y, x)))',
        '∀y.(∀z.(¬r¹(z) → ¬q²(y, z)) → p¹(y))',
        '∀z.∃z.(¬r¹(y) ∧ ¬r²(z, y))'
    ]
)
def test_rebuilding_formulas(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(parse_formula(formula, dummy_signature)) == formula


def test_parsing_unclosed_conjunction_parentheses() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_propositional_formula('(p ∧ q ∧')

    assert str(excinfo.value) == 'Binary connective formulas must have a closing parenthesis'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ q ∧
          │ ^^^^^^^^
    ''')


def test_parsing_unclosed_conjunction_parentheses_truncated() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_propositional_formula('(p ∧ q')

    assert str(excinfo.value) == 'Binary connective formulas must have a closing parenthesis'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ q
          │ ^^^^^^
    ''')


def test_parsing_invalid_conjunction() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_propositional_formula('(p ∧ )')

    assert str(excinfo.value) == 'Binary connective formulas must have a second subformula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (p ∧ )
          │ ^^^^^^
    ''')


def test_parsing_conjunction_with_term_inside(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(x ∧ q₀)', dummy_signature)

    assert str(excinfo.value) == 'The first argument of a connective formula must itself be a formula'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x ∧ q₀)
          │  ^
    ''')


def test_complex_unbalanced_formula(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('(∀x.(q²(z, x) → ¬r²(y, x) ∧ ¬p¹(z))', dummy_signature)

    assert str(excinfo.value) == 'Binary connective formulas must have a closing parenthesis'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (∀x.(q²(z, x) → ¬r²(y, x) ∧ ¬p¹(z))
          │     ^^^^^^^^^^^^^^^^^^^^^^^
    ''')


def test_lone_quantifier() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('∀')

    assert str(excinfo.value) == 'Expected a variable after the quantifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀
          │ ^
    ''')


def test_quantifier_with_invalid_variable(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('∀p⁰.p⁰', dummy_signature)

    assert str(excinfo.value) == 'Expected a variable after the quantifier'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀p⁰.p⁰
          │ ^^^
    ''')


def test_quantifier_with_no_dot(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('∀xp⁰', dummy_signature)

    assert str(excinfo.value) == 'Expected dot after variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀xp⁰
          │ ^^
    ''')


def test_quantifier_with_no_subformula(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('∀x.', dummy_signature)

    assert str(excinfo.value) == 'Unexpected end of input'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ∀x.
          │   ^
    ''')


@pytest_parametrize_lists(
    formula=[
        '∀y.∃z.(¬p¹(z) ∧ ∀x.(q²(z, x) → ¬r²(y, x)))',
        '∀y.∃z.(¬p¹(z) ∧ ∀x.(q²(z, x) → ¬r²(y, x)))',
        '∀y₀.(∀z.(¬r¹(z) → ¬q²(y₀, z)) → p¹(y₀))',
        '((∃x.p¹(x) ∧ ∃y.q¹(y)) ∨ (∃x.p¹(x) ∧ ∃y.q¹(y)))'
    ]
)
def test_reparsing_formulas(formula: str, dummy_signature: FormalLogicSignature) -> None:
    assert str(parse_formula(str(parse_formula(formula, dummy_signature)), dummy_signature)) == formula


@pytest_parametrize_lists(
    schema=[
        'φ',
        '(φ → ψ)',
        '(φ ∧ ψ)',
        '∀x.(φ ∧ ψ)'
    ]
)
def test_rebuild_schemas(schema: str) -> None:
    assert str(parse_formula_schema(schema)) == schema


def test_parsing_formula_placeholder_with_regular_parser() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula('φ', EMPTY_SIGNATURE)

    assert str(excinfo.value) == 'Placeholders are only allowed in schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ φ
          │ ^
    ''')


@pytest_parametrize_lists(
    rule=[
        '⫢ ψ',
        'φ ⫢ ψ',
        'φ₁, φ₂ ⫢ ψ',
        '[θ] φ ⫢ ψ'
    ]
)
def test_rebuilding_rules(rule: str) -> None:
    assert parse_natural_deduction_rule('name', rule).without_name() == rule


def test_parsing_empty_discharge_schema() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_natural_deduction_rule('name', '[] φ ⫢ ψ')

    assert str(excinfo.value) == 'Empty discharge assumptions are disallowed'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ [] φ ⫢ ψ
          │ ^^
        '''
    )


def test_parsing_discharge_schema_with_no_closing_bracket() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_natural_deduction_rule('name', '[θ φ ⫢ ψ')

    assert str(excinfo.value) == 'Unclosed brackets for discharge schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ [θ φ ⫢ ψ
          │ ^^
        '''
    )


def test_parsing_substitution_schema_with_no_connective() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term_schema_substitution_spec('x')

    assert str(excinfo.value) == 'Expected ↦ after the variable in a substitution'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x
          │ ^
        '''
    )


def test_parsing_eigenvariable_substitution_schema() -> None:
    parsed = parse_term_schema_substitution_spec('x ↦ y*')
    assert parsed == EigenvariableSchemaSubstitutionSpec(
        src=VariablePlaceholder(LatinIdentifier('x')),
        dest=VariablePlaceholder(LatinIdentifier('y'))
    )


def test_parsing_substitution_schema_with_star_on_term_placeholder() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term_schema_substitution_spec('x ↦ τ*')

    assert str(excinfo.value) == 'Cannot place an eigenvariable marker on a more general term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x ↦ τ*
          │      ^
        '''
    )


def test_parsing_substitution_schema_with_no_closing_bracket() -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_formula_schema_with_substitution('φ[x ↦ y')

    assert str(excinfo.value) == 'Unclosed brackets for substitution specification'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ φ[x ↦ y
          │ ^^^^^^^
        '''
    )
