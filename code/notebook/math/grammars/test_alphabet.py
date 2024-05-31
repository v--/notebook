from .alphabet import NonTerminal, new_non_terminal


def test_new_non_terminal() -> None:
    assert new_non_terminal('test', frozenset()) == NonTerminal('test₀')
    assert new_non_terminal('test', frozenset([NonTerminal('test₀')])) == NonTerminal('test₁')
    assert new_non_terminal('test₀', frozenset()) == NonTerminal('test₁')
