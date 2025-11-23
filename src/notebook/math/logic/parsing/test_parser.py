from textwrap import dedent

import pytest

from ....parsing import LatinIdentifier, ParserError, TokenizerError
from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..common import variables as var
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
        expected=FunctionApplication('f⁰', [])
    ),
    dict(
        term='f¹(x)',
        expected=FunctionApplication('f¹', [Variable(LatinIdentifier('x'))])
    ),
    dict(
        term='f³(x, y, z)',
        expected=FunctionApplication('f³', [Variable(LatinIdentifier(s)) for s in 'xyz'])
    ),
    dict(
        term='f³(x,y,  z)',
        expected=FunctionApplication('f³', [Variable(LatinIdentifier(s)) for s in 'xyz'])
    )
)
def test_parsing_valid_functions(term: str, expected: FunctionApplication, dummy_signature: FormalLogicSignature) -> None:
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

    assert str(excinfo.value) == 'Expected a term'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ p⁰
          │ ^^
    ''')


def test_parsing_zero_arity_function_with_empty_arg_list(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(ParserError) as excinfo:
        parse_term('f⁰()', dummy_signature)

    assert str(excinfo.value) == 'Avoid the argument list at all when zero arguments are expected'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f⁰()
          │ ^^^^
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

    assert str(excinfo.value) == 'Expected 2 arguments for f² but got 1'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ f²(x)
          │ ^^^^^
    ''')


@pytest_parametrize_kwargs(
    dict(
        formula='(x = y)',
        expected=EqualityFormula(var.x, var.y)
    ),
    dict(
        formula='(f¹(x) = f²(y, z))',
        expected=EqualityFormula(
            FunctionApplication('f¹', [var.x]),
            FunctionApplication('f²', [var.y, var.z]),
        )
    )
)
def test_parsing_valid_equalities(formula: str, expected: EqualityFormula, dummy_signature: FormalLogicSignature) -> None:
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
