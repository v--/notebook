import pytest

from .verbatim import is_verbatim_string, strip_outer_braces


@pytest.mark.parametrize(
    'string',
    [
        '{test}',
        '{t e s t}',
        '{t{e} {s}t}'
    ]
)
def test_is_verbatim_string_success(string: str) -> None:
    assert is_verbatim_string(string)


@pytest.mark.parametrize(
    'string',
    [
        'test',
        '{t e s t',
        '{te} {st}',
        '{t{e} s}t}'
    ]
)
def test_is_verbatim_string_failure(string: str) -> None:
    assert not is_verbatim_string(string)


@pytest.mark.parametrize(
    'string',
    [
        '{test',
        '{te} {st}',
        '{t{e} s}t}'
    ]
)
def test_strip_outer_braces_noop(string: str) -> None:
    assert strip_outer_braces(string) == string


@pytest.mark.parametrize(
    ('string', 'expected'),
    {
        '{test}': 'test',
        '{{test}}': '{test}',
    }.items()
)
def test_strip_outer_braces(string: str, expected: str) -> None:
    assert strip_outer_braces(string) == expected
