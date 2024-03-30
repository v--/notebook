from .conftest import assert_aabn, assert_leucine
from .finite import FiniteAutomaton


# ex:def:formal_language/an
def test_finite_automaton_recognizes_an():
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
def test_finite_automaton_recognizes_aabn(aabn: FiniteAutomaton):
    assert not aabn.is_deterministic()
    assert_aabn(aabn)


def test_finite_automaton_recognizes_leucine(leucine: FiniteAutomaton):
    assert not leucine.is_deterministic()
    assert_leucine(leucine)
