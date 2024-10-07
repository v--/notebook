from .conftest import FiniteAutomatonFixture
from .finite import FiniteAutomaton


# ex:def:formal_language/an
def test_finite_automaton_recognizes_an() -> None:
    aut: FiniteAutomaton = FiniteAutomaton()
    aut.add_transition(1, 'a', 1)
    aut.initial.add(1)
    aut.terminal.add(1)

    assert aut.is_deterministic()

    assert aut.recognize('')
    assert aut.recognize('a')
    assert aut.recognize('aaaaaaaaaaaaaaaaaaaa')
    assert not aut.recognize('b')
    assert not aut.recognize('ab')


# fig:def:finite_automaton
def test_finite_automaton_recognizes_aabn(aabn: FiniteAutomatonFixture) -> None:
    assert not aabn.aut.is_deterministic()
    aabn.assert_equivalent(aabn.aut)


def test_finite_automaton_recognizes_leucine(leucine: FiniteAutomatonFixture) -> None:
    assert not leucine.aut.is_deterministic()
    leucine.assert_equivalent(leucine.aut)
