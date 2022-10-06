import pytest

from .grammar import Epsilon, Grammar, GrammarRule, GrammarSchema, NonTerminal, Terminal


@pytest.fixture
def an():
    schema = GrammarSchema()
    schema.add_rule('<S> → ε')
    schema.add_rule('<S> → <A>')
    schema.add_rule('<A> → <A> "a"')
    schema.add_rule('<A> → "a"')
    return schema.instantiate_grammar('S')


@pytest.fixture
def anbn():
    schema = GrammarSchema()
    schema.add_rule('<S> → ε')
    schema.add_rule('<S> → <A>')
    schema.add_rule('<A> → "a" <A> "b"')
    schema.add_rule('<A> → "a" "b"')
    return schema.instantiate_grammar('S')


def test_an(an: Grammar):
    assert an.schema.rules == {
        GrammarRule([NonTerminal('S')], [Epsilon()]),
        GrammarRule([NonTerminal('S')], [NonTerminal('A')]),
        GrammarRule([NonTerminal('A')], [NonTerminal('A'), Terminal('a')]),
        GrammarRule([NonTerminal('A')], [Terminal('a')]),
    }

    assert an.schema.get_terminals() == {Terminal('a')}
    assert an.schema.get_non_terminals() == {NonTerminal('S'), NonTerminal('A')}
