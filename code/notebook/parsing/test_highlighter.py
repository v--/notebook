from dataclasses import dataclass
from textwrap import dedent

from .highlighter import ErrorHighlighter


def test_error_basic():
    highlighter = ErrorHighlighter(
        'test',
        i_first_token=1,
        i_last_token=1
    )

    assert highlighter.highlight() == dedent('''\
        1 │ test
          │  ^
        '''
    )


def test_error_on_end():
    highlighter = ErrorHighlighter(
        'test\n',
        i_first_token=4,
        i_last_token=4
    )

    assert highlighter.highlight() == dedent('''\
        1 │ test↵
          │     ^
        '''
    )


def test_error_multiline_basic():
    highlighter = ErrorHighlighter(
        'test1\ntest2\ntest3',
        i_first_token=7,
        i_last_token=7
    )

    assert highlighter.highlight() == dedent('''\
        2 │ test2↵
          │  ^
        '''
    )


def test_error_multiline_succeed():
    highlighter = ErrorHighlighter(
        'test1\ntest2\ntest3',
        i_first_token=7,
        i_last_token=15
    )

    assert highlighter.highlight() == dedent('''\
        2 │ test2↵
          │  ^^^^^
        3 │ test3
          │ ^^^^
        '''
    )


@dataclass
class StringWrapper:
    payload: str

    def __str__(self):
        return self.payload


def test_string_wrapper_basic():
    highlighter = ErrorHighlighter(
        [StringWrapper('test1')],
        i_first_token=0,
        i_last_token=0
    )

    assert highlighter.highlight() == dedent('''\
        1 │ test1
          │ ^^^^^
        '''
    )


def test_string_wrapper_with_line_break():
    highlighter = ErrorHighlighter(
        [
            StringWrapper('test1\n'),
            StringWrapper('test2\n'),
            StringWrapper('test3')
        ],
        i_first_token=1,
        i_last_token=1
    )

    assert highlighter.highlight() == dedent('''\
        2 │ test2↵
          │ ^^^^^^
        '''
    )
