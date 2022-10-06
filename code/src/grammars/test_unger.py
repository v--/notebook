from .grammar import Grammar
from .unger import iter_partitions, parse
from .fixtures import *


def test_iter_partitions():
    assert sorted(iter_partitions('asdf', 1)) == [['asdf']]
    assert sorted(iter_partitions('asdf', 2)) == [['', 'asdf'], ['a', 'sdf'], ['as', 'df'], ['asd', 'f'], ['asdf', '']]
    assert ['asdf', '', '', '', ''] in sorted(iter_partitions('asdf', 5))
    assert ['', 'as', '', 'df', ''] in sorted(iter_partitions('asdf', 5))


def assert_word_rebuilt(grammar: Grammar, string: str):
    tree = parse(grammar, string)
    assert tree is not None
    assert tree.yield_word() == string


def assert_word_invalid(grammar: Grammar, string: str):
    tree = parse(grammar, string)
    if tree:
        from rich import print
        print(tree.build_rich_tree())
    assert tree is None


def test_an(an: Grammar):
    assert_word_rebuilt(an, '')
    assert_word_rebuilt(an, 'a')
    assert_word_rebuilt(an, 'aaa')

    assert_word_invalid(an, 'b')
    assert_word_invalid(an, 'ab')


def test_anbn(anbn: Grammar):
    assert_word_rebuilt(anbn, '')
    assert_word_rebuilt(anbn, 'ab')
    assert_word_rebuilt(anbn, 'aaabbb')

    assert_word_invalid(anbn, 'a')
    assert_word_invalid(anbn, 'ba')


def test_epsilon_rules(s3):
    assert_word_rebuilt(s3, '')
    assert_word_rebuilt(s3, 'a')
    assert_word_rebuilt(s3, 'aa')
    assert_word_rebuilt(s3, 'aaa')

    assert_word_invalid(s3, 'b')
