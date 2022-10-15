from .grammar import Grammar
from .unger import iter_partitions, parse
from .fixtures import *


def assert_word_rebuilt(grammar: Grammar, string: str):
    trees = list(parse(grammar, string))
    assert len(trees) > 0

    for tree in trees:
        if tree.yield_word() != string:
            print(tree)

        assert tree.yield_word() == string


def assert_word_invalid(grammar: Grammar, string: str):
    trees = list(parse(grammar, string))

    if len(trees) > 0:
        for tree in trees:
            print(tree)

    assert len(trees) == 0


def test_iter_partitions():
    assert sorted(iter_partitions('asdf', 1)) == [['asdf']]
    assert sorted(iter_partitions('asdf', 2)) == [['', 'asdf'], ['a', 'sdf'], ['as', 'df'], ['asd', 'f'], ['asdf', '']]
    assert ['asdf', '', '', '', ''] in sorted(iter_partitions('asdf', 5))
    assert ['', 'as', '', 'df', ''] in sorted(iter_partitions('asdf', 5))


def test_an_valid(an: Grammar):
    assert_word_rebuilt(an, '')
    assert_word_rebuilt(an, 'a')
    assert_word_rebuilt(an, 'aaa')


def test_an_invalid(an: Grammar):
    assert_word_invalid(an, 'b')
    assert_word_invalid(an, 'ab')


def test_anbn_valid(anbn: Grammar):
    assert_word_rebuilt(anbn, '')
    assert_word_rebuilt(anbn, 'ab')
    assert_word_rebuilt(anbn, 'aaabbb')


def test_anbn_invalid(anbn: Grammar):
    assert_word_invalid(anbn, 'a')
    assert_word_invalid(anbn, 'ba')


def test_epsilon_rules_valid(s3: Grammar):
    assert_word_rebuilt(s3, '')
    assert_word_rebuilt(s3, 'a')
    assert_word_rebuilt(s3, 'aa')
    assert_word_rebuilt(s3, 'aaa')


def test_epsilon_rules_invalid(s3: Grammar):
    assert_word_invalid(s3, 'b')


def test_binary_numbers_valid(binary: Grammar):
    assert_word_rebuilt(binary, '0')
    assert_word_rebuilt(binary, '1')
    assert_word_rebuilt(binary, '10')
    assert_word_rebuilt(binary, '11')
    assert_word_rebuilt(binary, '100')
    assert_word_rebuilt(binary, '101')


def test_binary_numbers_invalid(binary: Grammar):
    assert_word_invalid(binary, '')
    assert_word_invalid(binary, '01')
