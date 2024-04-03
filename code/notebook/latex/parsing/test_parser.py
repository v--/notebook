from textwrap import dedent

import pytest

from ...parsing.parser import ParsingError
from ...parsing.whitespace import Whitespace
from ..nodes import (
    BraceGroup,
    BracketGroup,
    Command,
    Environment,
    Word,
    stringify_nodes,
)
from .parser import parse_latex


def test_empty_string() -> None:
    string = ''
    nodes = parse_latex(string)
    assert nodes == []


def test_tab() -> None:
    string = '\t'
    nodes = parse_latex(string)
    assert nodes == [Whitespace.tab]


def test_line_break() -> None:
    string = '\n'
    nodes = parse_latex(string)
    assert nodes == [Whitespace.line_break]


def test_word() -> None:
    string = 'test'
    nodes = parse_latex(string)
    assert nodes == [Word(value='test')]


def test_command_without_args() -> None:
    string = r'\test'
    nodes = parse_latex(string)
    assert nodes == [Command('test')]


def test_command_with_space() -> None:
    string = r'\test '
    nodes = parse_latex(string)
    assert nodes == [
        Command('test'),
        Whitespace.space
    ]


def test_command_with_brace_arg() -> None:
    string = r'\test{a}'
    nodes = parse_latex(string)
    assert nodes == [
        Command('test'),
        BraceGroup([Word('a')])
    ]


def test_unmatched_brace() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_latex('\\test{a')

    assert str(excinfo.value) == 'Unmatched {'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \test{a
          │      ^^
        '''[1:]
    )



def test_command_with_bracket_arg() -> None:
    string = '\\test[a]'
    nodes = parse_latex(string)
    assert nodes == [
        Command('test'),
        BracketGroup([Word('a')])
    ]


def test_unmatched_bracket() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_latex('\\test[a')

    assert str(excinfo.value) == 'Unmatched ['
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \test[a
          │      ^^
        '''[1:]
    )


def test_command_with_mixed_args() -> None:
    string = '\\test\t[a]{b} [c ] \n{d}'
    nodes = parse_latex(string)
    assert nodes == [
        Command('test'),
        Whitespace.tab,
        BracketGroup([Word('a')]),
        BraceGroup([Word('b')]),
        Whitespace.space,
        BracketGroup([
            Word('c'),
            Whitespace.space
        ]),
        Whitespace.space,
        Whitespace.line_break,
        BraceGroup([Word('d')]),
    ]


def test_basic_environment() -> None:
    string = r'\begin{test} \end{test}'
    nodes = parse_latex(string)

    assert len(nodes) == 1
    assert nodes[0] == Environment(
        name='test',
        contents=[
            Whitespace.space
        ]
    )


def test_unmatched_environment() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_latex(r'\begin{test}')

    assert str(excinfo.value) == "Unmatched environment 'test'"
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \begin{test}
          │ ^^^^^^^^^^^^
        '''[1:]
    )


def test_mismatched_environment() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_latex(
            dedent(r'''
                \begin{test}
                \end{tes}
                '''[1:]
            )
        )

    assert str(excinfo.value) == "Mismatched environment 'test'"
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \begin{test}↵
          │ ^^^^^^^^^^^^^
        2 │ \end{tes}↵
          │ ^^^^^^^^^
        '''[1:]
    )


def test_missing_environment_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_latex(r'\begin')

    assert str(excinfo.value) == 'No environment name specified'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \begin
          │ ^^^^^^
        '''[1:]
    )


def test_unclosed_and_missing_environment_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_latex(r'\begin{')

    assert str(excinfo.value) == 'No environment name specified'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \begin{
          │ ^^^^^^^
        '''[1:]
    )


def test_invalid_environment_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_latex(r'\begin{&}')

    assert str(excinfo.value) == 'No environment name specified'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \begin{&}
          │ ^^^^^^^^
        '''[1:]
    )


def test_unclosed_environment_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_latex(r'\begin{test')

    assert str(excinfo.value) == 'Unclosed brace when specifying environment name'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ \begin{test
          │        ^^^^
        '''[1:]
    )


def test_different_nested_environments() -> None:
    string = '\\begin{test} \\begin{test2} inner \\end{test2} \\end{test}'
    nodes = parse_latex(string)

    assert len(nodes) == 1
    assert nodes[0] == Environment(
        name='test',
        contents=[
            Whitespace.space,
            Environment(
                name='test2',
                contents=[
                    Whitespace.space,
                    Word('inner'),
                    Whitespace.space
                ]
            ),
            Whitespace.space
        ]
    )


def test_same_nested_environment() -> None:
    string = '\\begin{test} \\begin{test} inner \\end{test} \\end{test}'
    nodes = parse_latex(string)

    assert len(nodes) == 1
    assert nodes[0] == Environment(
        name='test',
        contents=[
            Whitespace.space,
            Environment(
                name='test',
                contents=[
                    Whitespace.space,
                    Word('inner'),
                    Whitespace.space
                ]
            ),
            Whitespace.space
        ]
    )


def test_matrix_environment() -> None:
    string = dedent(r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
        '''
    )

    nodes = parse_latex(string)
    assert ''.join(map(str, nodes)) == string


def test_real() -> None:
    with open('../figures/thm__natural_number_divisibility_order.tex') as file:  # noqa: PTH123
        string = file.read()
        nodes = parse_latex(string)
        assert stringify_nodes(nodes) == string
