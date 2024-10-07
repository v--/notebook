from .alphabet import NonTerminal, Terminal
from .conftest import GrammarFixture
from .grammar import GrammarRule


def test_an(an: GrammarFixture) -> None:
    schema = an.grammar.schema

    assert schema.rules == [
        GrammarRule([NonTerminal('S')], []),
        GrammarRule([NonTerminal('S')], [NonTerminal('A')]),
        GrammarRule([NonTerminal('A')], [NonTerminal('A'), Terminal('a')]),
        GrammarRule([NonTerminal('A')], [Terminal('a')]),
    ]

    assert schema.get_terminals() == {Terminal('a')}
    assert schema.get_non_terminals() == {NonTerminal('S'), NonTerminal('A')}
