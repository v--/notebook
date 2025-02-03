from textwrap import dedent

import pytest

from ....parsing.identifiers import LatinIdentifier
from ....parsing.parser import ParsingError
from ....support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from ..alphabet import BinaryTypeConnective
from ..assertions import TypeAssertion
from ..signature import EMPTY_SIGNATURE
from ..terms import Constant, TypedAbstraction, UntypedApplication, Variable
from ..type_systems import HOL_SIGNATURE
from ..types import BaseType, SimpleConnectiveType, SimpleType
from .parser import (
    TypingStyle,
    parse_pure_term,
    parse_term,
    parse_term_schema,
    parse_type,
    parse_type_assertion,
    parse_type_schema,
    parse_typing_rule,
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
    assert parse_pure_term(term) == expected


def test_parsing_long_variable_names() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('xy')

    assert str(excinfo.value) == 'Finished parsing but there is still input left'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ xy
          │  ^
        '''
    )


def test_parsing_invalid_variable_suffix() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('x₀₁')

    assert str(excinfo.value) == 'Nonzero natural numbers cannot start with zero'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x₀₁
          │  ^^
        '''
    )


@pytest_parametrize_kwargs(
    dict(
        term='Q',
        expected=Constant('Q')
    ),
    dict(
        term='(I(Qx))',
        expected=UntypedApplication(
            Constant('I'),
            UntypedApplication(Constant('Q'), Variable(LatinIdentifier('x')))
        )
    )
)
def test_parsing_constants(term: str, expected: Constant) -> None:
    assert parse_term(HOL_SIGNATURE, term, typing=TypingStyle.explicit) == expected


@pytest_parametrize_lists(
    term=[
        'x',
        '(xy)',
        '(x₁y₂)',
        '(λx.x)', # I combinator
        '(λx.y)',
        '(λx.(λy.x))', # K combinator
        '(λx.(λy.(λz.((xz)(yz)))))', # S combinator
        '(λf.((λx.(f(xx)))(λx.(f(xx)))))', # Y combinator
    ]
)
def test_rebuilding_terms(term: str) -> None:
    assert str(parse_pure_term(term)) == term


def test_parsing_abstraction_with_unclosed_parens() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('(λx.x')

    assert str(excinfo.value) == 'Unclosed parentheses for abstraction'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λx.x
          │ ^^^^^
        '''
    )


def test_parsing_abstraction_with_unclosed_parens_truncated() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('(λ')

    assert str(excinfo.value) == 'Expected a variable name after λ'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λ
          │ ^^
        '''
    )


def test_parsing_abstraction_with_no_dot() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('(λxx)')

    assert str(excinfo.value) == 'Expected a dot after an abstraction variable'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λxx)
          │ ^^^^
        '''
    )


def test_parsing_empty_application() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('()')

    assert str(excinfo.value) == 'Applications must have two terms, while abstractions must begin with λ'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ ()
          │ ^^
        '''
    )


def test_parsing_incomplete_application() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('(x)')

    assert str(excinfo.value) == 'Applications must have a second subterm'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (x)
          │ ^^^
        '''
    )


@pytest_parametrize_lists(
    term=[
        '(λx.(λy.x))', # K combinator
        '(λx.(λy.(λz.((xz)(yz)))))', # S combinator
        '(λf.((λx.(f(xx)))(λx.(f(xx)))))', # Y combinator
    ]
)
def test_reparsing_terms(term: str) -> None:
    assert str(parse_pure_term(str(parse_pure_term(term)))) == term


@pytest_parametrize_lists(
    term=[
        'x',
        'Q',
        '(Qx)',
        '(λx:ι.(Qx))',
    ]
)
def test_rebuilding_term_with_constants(term: str) -> None:
    assert str(parse_term(HOL_SIGNATURE, term, typing=TypingStyle.explicit)) == term


@pytest_parametrize_lists(
    schema=[
        'x',
        'Q', # PlainConstant
        'M', # Placeholder
        '(QM)',
        '(λx.(QM))',
    ]
)
def test_rebuilding_schema(schema: str) -> None:
    assert str(parse_term_schema(HOL_SIGNATURE, schema, typing=TypingStyle.implicit)) == schema


def test_parsing_term_schema_with_regular_parser() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_pure_term('M')

    assert str(excinfo.value) == 'Term placeholders are only allowed in schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ M
          │ ^
        '''
    )


@pytest_parametrize_kwargs(
    dict(
        type_='ι',
        expected=BaseType('ι')
    ),
    dict(
        type_='(ι → o)',
        expected=SimpleConnectiveType(
            BinaryTypeConnective.arrow,
            BaseType('ι'),
            BaseType('o')
        )
    ),
    dict(
        type_='(ι → (ι → o))',
        expected=SimpleConnectiveType(
            BinaryTypeConnective.arrow,
            BaseType('ι'),
            SimpleConnectiveType(
                BinaryTypeConnective.arrow,
                BaseType('ι'),
                BaseType('o')
            )
        )
    )
)
def test_parsing_valid_type(type_: str, expected: SimpleType) -> None:
    assert parse_type(HOL_SIGNATURE, type_) == expected


@pytest_parametrize_lists(
    # ι and o are base types, the rest are placeholders
    schema=[
        'ι',
        '(ι → o)',
        'α',
        '(β → β)',
        '(ι → (α → β))',
        '((ι → α) → β)'
    ]
)
def test_rebuilding_type_schema(schema: str) -> None:
    assert str(parse_type_schema(HOL_SIGNATURE, schema)) == schema


def test_parsing_type_schema_with_regular_parser() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_type(HOL_SIGNATURE, 'α')

    assert str(excinfo.value) == 'Type placeholders are only allowed in schemas'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ α
          │ ^
        '''
    )


def test_parsing_type_assertion_missing_arrow() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_type(HOL_SIGNATURE, '(ι o)')

    assert str(excinfo.value) == 'Binary types must have a connective after the first subtype'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (ι o)
          │ ^^^^
        '''
    )


def test_parsing_typed_abstraction() -> None:
    var = Variable(LatinIdentifier('x'))
    var_type = BaseType('ι')
    expected = TypedAbstraction(var, var, var_type)
    assert parse_term(HOL_SIGNATURE, '(λx:ι.x)', typing=TypingStyle.explicit) == expected


def test_parsing_typed_abstraction_with_untyped_parser() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(HOL_SIGNATURE, '(λx:ι.x)', typing=TypingStyle.implicit)

    assert str(excinfo.value) == 'Unexpected type annotation for the abstractor variable in an untyped abstraction'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λx:ι.x)
          │    ^
        '''
    )


def test_parsing_untyped_abstraction_with_typed_parser() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_term(HOL_SIGNATURE, '(λx.x)', typing=TypingStyle.explicit)

    assert str(excinfo.value) == 'Expected a type annotation for the abstractor variable in a typed abstraction'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (λx.x)
          │    ^
        '''
    )


@pytest_parametrize_lists(
    assertion=[
        'x: ι',
        'p: (ι → ι)',
        'f: (ι → o)'
    ]
)
def test_parsing_type_assertion(assertion: str) -> None:
    term, type_ = assertion.split(': ', maxsplit=2)
    expected = TypeAssertion(
        parse_term(HOL_SIGNATURE, term, typing=TypingStyle.explicit),
        parse_type(HOL_SIGNATURE, type_)
    )

    assert parse_type_assertion(HOL_SIGNATURE, assertion, typing=TypingStyle.explicit) == expected


def test_parsing_type_assertion_missing_colon() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_type_assertion(HOL_SIGNATURE, 'x ι', typing=TypingStyle.explicit)

    assert str(excinfo.value) == 'Expected a colon after the term in a type specification'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ x ι
          │ ^^
        '''
    )


@pytest_parametrize_lists(
    rule=[
        '(R) ⫢ x: α',
        '(R) M: (α → β), N: α ⫢ (MN): β',
        '(R) [x: α] M: β ⫢ (λx.M): (α → β)'
    ]
)
def test_rebuilding_typing_rules(rule: str) -> None:
    assert str(parse_typing_rule(EMPTY_SIGNATURE, rule)) == rule


def test_parsing_discharge_schema_with_no_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_typing_rule(EMPTY_SIGNATURE, '(R) [] x: α ⫢ y: α')

    assert str(excinfo.value) == 'Unexpected token'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [] x: α ⫢ y: α
          │      ^
        '''
    )


def test_parsing_discharge_schema_with_no_closing_bracket() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_typing_rule(EMPTY_SIGNATURE, '(R) [x: α y: α ⫢ z: α')

    assert str(excinfo.value) == 'Unclosed bracket for discharge schema'
    assert excinfo.value.__notes__[0] == dedent('''\
        1 │ (R) [x: α y: α ⫢ z: α
          │     ^^^^^^
        '''
    )
