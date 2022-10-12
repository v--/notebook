from .grammar import Grammar
from .unger import parse
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
    assert len(trees) == 0


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


def test_epsilon_rules_valid(s3):
    assert_word_rebuilt(s3, '')
    assert_word_rebuilt(s3, 'a')
    assert_word_rebuilt(s3, 'aa')
    assert_word_rebuilt(s3, 'aaa')


def test_epsilon_rules_invalid(s3):
    assert_word_invalid(s3, 'b')
