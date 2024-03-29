from .grammar import SingletonSymbol, Grammar, GrammarRule, NonTerminal, Terminal


def test_an(an: Grammar):
    assert an.schema.rules == [
        GrammarRule([NonTerminal('S')], [SingletonSymbol.epsilon]),
        GrammarRule([NonTerminal('S')], [NonTerminal('A')]),
        GrammarRule([NonTerminal('A')], [NonTerminal('A'), Terminal('a')]),
        GrammarRule([NonTerminal('A')], [Terminal('a')]),
    ]

    assert an.schema.get_terminals() == {Terminal('a')}
    assert an.schema.get_non_terminals() == {NonTerminal('S'), NonTerminal('A')}
