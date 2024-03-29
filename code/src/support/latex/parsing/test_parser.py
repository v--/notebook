import pytest

from ...parsing.parser import ParserError
from ..nodes import Command, BracelessGroup, BraceGroup, BracketGroup, Word, Whitespace, Environment
from .parser import parse_latex


def test_empty_string():
    string = ''
    node = parse_latex(string)
    assert node == BracelessGroup([])


def test_space():
    string = '\t'
    node = parse_latex(string)
    assert node == Whitespace(value='\t')


def test_newline():
    string = '\n'
    node = parse_latex(string)
    assert node == Whitespace(value='\n')


def test_word():
    string = 'test'
    node = parse_latex(string)
    assert node == Word(value='test')


def test_command_without_args():
    string = '\\test'
    node = parse_latex(string)
    assert node == Command('test')


def test_command_with_space():
    string = '\\test '
    node = parse_latex(string)
    assert node == BracelessGroup([
        Command('test'),
        Whitespace(' ')
    ])


def test_command_with_brace_arg():
    string = '\\test{a}'
    node = parse_latex(string)
    assert node == BracelessGroup([
        Command('test'),
        BraceGroup([Word('a')])
    ])


def test_unmatched_brace():
    string = '\\test{a'

    with pytest.raises(ParserError):
        parse_latex(string)


def test_command_with_bracket_arg():
    string = '\\test[a]'
    node = parse_latex(string)
    assert node == BracelessGroup([
        Command('test'),
        BracketGroup([Word('a')])
    ])


def test_unmatched_bracket():
    string = '\\test[a'

    with pytest.raises(ParserError):
        parse_latex(string)


def test_command_with_mixed_args():
    string = '\\test\t[a]{b} [c ] \n{d}'
    node = parse_latex(string)
    assert node == BracelessGroup([
        Command('test'),
        Whitespace('\t'),
        BracketGroup([Word('a')]),
        BraceGroup([Word('b')]),
        Whitespace(' '),
        BracketGroup([
            Word('c'),
            Whitespace(' ')
        ]),
        Whitespace(' '),
        Whitespace('\n'),
        BraceGroup([Word('d')]),
    ])


def test_basic_environment():
    string = '\\begin{test} \\end{test}'
    node = parse_latex(string)
    assert node == Environment(
        name='test',
        contents=[
            Whitespace(' ')
        ]
    )


def test_unmatched_environment():
    string = '\\begin{test}'

    with pytest.raises(ParserError):
        parse_latex(string)


def test_missing_environment_name():
    string = '\\begin'

    with pytest.raises(ParserError):
        parse_latex(string)


def test_unclosed_and_missing_environment_name():
    string = '\\begin{'

    with pytest.raises(ParserError):
        parse_latex(string)


def test_unclosed_environment_name():
    string = '\\begin{test'

    with pytest.raises(ParserError):
        parse_latex(string)


def test_different_nested_environments():
    string = '\\begin{test} \\begin{test2} inner \\end{test2} \\end{test}'
    node = parse_latex(string)
    assert node == Environment(
        name='test',
        contents=[
            Whitespace(' '),
            Environment(
                name='test2',
                contents=[
                    Whitespace(' '),
                    Word('inner'),
                    Whitespace(' ')
                ]
            ),
            Whitespace(' ')
        ]
    )


def test_same_nested_environment():
    string = '\\begin{test} \\begin{test} inner \\end{test} \\end{test}'
    node = parse_latex(string)
    assert node == Environment(
        name='test',
        contents=[
            Whitespace(' '),
            Environment(
                name='test',
                contents=[
                    Whitespace(' '),
                    Word('inner'),
                    Whitespace(' ')
                ]
            ),
            Whitespace(' ')
        ]
    )


def test_matrix_environment():
    string = r'''
        \begin{pmatrix}
          1 & 0 \\
          0 & 1
        \end{pmatrix}
    '''
    node = parse_latex(string)
    assert str(node) == string


def test_real():
    with open('../figures/thm__natural_number_divisibility_order.tex') as file:
        string = file.read()
        node = parse_latex(string)
        assert str(node) == string
