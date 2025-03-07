from textwrap import dedent

from .highlighter import ErrorHighlighter


def test_error_basic() -> None:
    highlighter = ErrorHighlighter(
        'test',
        offset_hi_start=1,
        offset_hi_end=1
    )

    assert highlighter.highlight() == dedent('''\
        1 │ test
          │  ^
        '''
    )


def test_error_on_end() -> None:
    highlighter = ErrorHighlighter(
        'test\n',
        offset_hi_start=4,
        offset_hi_end=4
    )

    assert highlighter.highlight() == dedent('''\
        1 │ test↵
          │     ^
        '''
    )


def test_error_multiline_excerpt() -> None:
    highlighter = ErrorHighlighter(
        'test1\ntest2\ntest3',
        offset_hi_start=7,
        offset_hi_end=7
    )

    assert highlighter.highlight() == dedent('''\
        2 │ test2↵
          │  ^
        '''
    )


def test_error_multiline() -> None:
    highlighter = ErrorHighlighter(
        'test1\ntest2\ntest3',
        offset_hi_start=7,
        offset_hi_end=15
    )

    assert highlighter.highlight() == dedent('''\
        2 │ test2↵
          │  ^^^^^
        3 │ test3
          │ ^^^^
        '''
    )


def test_error_multiline_wide_visibility() -> None:
    highlighter = ErrorHighlighter(
        'test1\ntest2\ntest3\ntest4\ntest5',
        offset_hi_start=7,
        offset_hi_end=15,
        offset_shown_start=0,
        offset_shown_end=25,
    )

    assert highlighter.highlight() == dedent('''\
        1 │ test1↵
        2 │ test2↵
          │  ^^^^^
        3 │ test3↵
          │ ^^^^
        4 │ test4↵
        5 │ test5
        '''
    )
