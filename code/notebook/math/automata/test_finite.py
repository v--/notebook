from .conftest import FiniteAutomatonFixture
from .finite import FiniteAutomaton


# ex:def:formal_language/an
def test_finite_automaton_recognizes_an() -> None:
    aut: FiniteAutomaton = FiniteAutomaton()
    aut.add_transition(src=1, dest=1, symbol='a')
    aut.initial.add(1)
    aut.terminal.add(1)

    assert aut.recognize('')
    assert aut.recognize('a')
    assert aut.recognize('aaaaaaaaaaaaaaaaaaaa')
    assert not aut.recognize('b')
    assert not aut.recognize('ab')


# fig:def:finite_automaton
def test_finite_automaton_recognizes_aabn(aabn: FiniteAutomatonFixture) -> None:
    aabn.assert_equivalent(aabn.aut)


def test_finite_automaton_recognizes_leucine(leucine: FiniteAutomatonFixture) -> None:
    leucine.assert_equivalent(leucine.aut)
