from .brute_force_parse import iter_partitions, parse
from .grammar import Grammar


def assert_string_rebuilt(grammar: Grammar, string: str) -> None:
    trees = list(parse(grammar, string))
    assert len(trees) > 0

    for tree in trees:
        if tree.yield_string() != string:
            pass

        assert tree.yield_string() == string


def assert_string_invalid(grammar: Grammar, string: str) -> None:
    trees = list(parse(grammar, string))

    if len(trees) > 0:
        for _tree in trees:
            pass

    assert len(trees) == 0


def test_iter_partitions() -> None:
    assert sorted(iter_partitions('asdf', 1)) == [['asdf']]
    assert sorted(iter_partitions('asdf', 2)) == [['', 'asdf'], ['a', 'sdf'], ['as', 'df'], ['asd', 'f'], ['asdf', '']]
    assert ['asdf', '', '', '', ''] in sorted(iter_partitions('asdf', 5))
    assert ['', 'as', '', 'df', ''] in sorted(iter_partitions('asdf', 5))


def test_an_valid(an: Grammar) -> None:
    assert_string_rebuilt(an, '')
    assert_string_rebuilt(an, 'a')
    assert_string_rebuilt(an, 'aaa')


def test_an_invalid(an: Grammar) -> None:
    assert_string_invalid(an, 'b')
    assert_string_invalid(an, 'ab')


def test_anbn_valid(anbn: Grammar) -> None:
    assert_string_rebuilt(anbn, '')
    assert_string_rebuilt(anbn, 'ab')
    assert_string_rebuilt(anbn, 'aaabbb')


def test_anbn_invalid(anbn: Grammar) -> None:
    assert_string_invalid(anbn, 'a')
    assert_string_invalid(anbn, 'ba')


def test_epsilon_rules_valid(s3: Grammar) -> None:
    assert_string_rebuilt(s3, '')
    assert_string_rebuilt(s3, 'a')
    assert_string_rebuilt(s3, 'aa')
    assert_string_rebuilt(s3, 'aaa')


def test_epsilon_rules_invalid(s3: Grammar) -> None:
    assert_string_invalid(s3, 'b')


def test_binary_numbers_valid(binary: Grammar) -> None:
    assert_string_rebuilt(binary, '0')
    assert_string_rebuilt(binary, '1')
    assert_string_rebuilt(binary, '10')
    assert_string_rebuilt(binary, '11')
    assert_string_rebuilt(binary, '100')
    assert_string_rebuilt(binary, '101')


def test_binary_numbers_invalid(binary: Grammar) -> None:
    assert_string_invalid(binary, '')
    assert_string_invalid(binary, '01')
