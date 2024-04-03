from .alphabet import NonTerminal, Terminal
from .grammar import Grammar, GrammarRule


def test_an(an: Grammar) -> None:
    assert an.schema.rules == [
        GrammarRule([NonTerminal('S')], []),
        GrammarRule([NonTerminal('S')], [NonTerminal('A')]),
        GrammarRule([NonTerminal('A')], [NonTerminal('A'), Terminal('a')]),
        GrammarRule([NonTerminal('A')], [Terminal('a')]),
    ]

    assert an.schema.get_terminals() == {Terminal('a')}
    assert an.schema.get_non_terminals() == {NonTerminal('S'), NonTerminal('A')}
