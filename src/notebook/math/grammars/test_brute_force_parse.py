from collections.abc import Iterable, Sequence

import pytest

from ...support.pytest import pytest_parametrize_kwargs, pytest_parametrize_lists
from .brute_force_parse import derives, iter_partitions, parse


@pytest_parametrize_kwargs(
    dict(
        string='asdf',
        m=1,
        expected=[['asdf']]
    ),
    dict(
        string='asdf',
        m=2,
        expected=[['', 'asdf'], ['a', 'sdf'], ['as', 'df'], ['asd', 'f'], ['asdf', '']]
    )
)
def test_iter_partitions_match(string: str, m: int, expected: Iterable[Sequence[str]]) -> None:
    assert list(iter_partitions(string, m)) == expected


@pytest_parametrize_kwargs(
    dict(
        string='asdf',
        m=5,
        sublist=['asdf', '', '', '', '']
    ),
    dict(
        string='asdf',
        m=5,
        sublist=['', 'as', '', 'df', '']
    )
)
def test_iter_partitions_sublist(string: str, m: int, sublist: Iterable[Sequence[str]]) -> None:
    assert sublist in list(iter_partitions(string, m))


@pytest_parametrize_lists(
    grammar_name=['an', 'anbn', 's3', 'binary']
)
def test_parsing_valid(grammar_name: str, request: pytest.FixtureRequest) -> None:
    grammar, whitelist, _ = request.getfixturevalue(grammar_name)

    for string in whitelist:
        for tree in parse(grammar, string):
            assert tree.yield_string() == string


@pytest_parametrize_lists(
    grammar_name=['an', 'anbn', 's3', 'binary']
)
def test_parsing_invalid(grammar_name: str, request: pytest.FixtureRequest) -> None:
    grammar, _, blacklist = request.getfixturevalue(grammar_name)

    for string in blacklist:
        not derives(grammar, string)
