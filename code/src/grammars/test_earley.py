from .grammar import Grammar, GrammarSchema
from .earley import EarleyParser

from .test_grammar import an, anbn


def is_word_rebuilt(grammar: Grammar, string: str):
    EarleyParser(string, grammar).build_table()


def test_an(an: Grammar):
    is_word_rebuilt(an, '')
    is_word_rebuilt(an, 'a')
    is_word_rebuilt(an, 'aaa')


def test_anbn(anbn: Grammar):
    is_word_rebuilt(anbn, '')
    is_word_rebuilt(anbn, 'ab')
    is_word_rebuilt(anbn, 'aaabbb')


def test_empty_rules():
    schema = GrammarSchema()
    schema.add_rule('<S> → <S> <S>')
    schema.add_rule('<S> → ε')
    schema.add_rule('<S> → "a"')
    g = schema.instantiate_grammar('S')
    is_word_rebuilt(g, '')
    is_word_rebuilt(g, 'a')
    is_word_rebuilt(g, 'aaa')
