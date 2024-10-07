from .conftest import FiniteAutomatonFixture
from .finite import FiniteAutomaton
from .finite_determinize import determinize


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
def test_determinize_preserves_parallel_arcs() -> None:
    aut: FiniteAutomaton = FiniteAutomaton()
    aut.add_transition(1, 'a', 2)
    aut.add_transition(1, 'b', 2)
    aut.add_transition(1, 'a', 3)
    aut.add_transition(1, 'b', 3)
    aut.add_transition(2, 'b', 3)
    aut.initial.add(1)
    aut.terminal.add(3)

    det = determinize(aut)

    assert {'a', 'b'} == {
        label
        for src, label, dest in det.triples
        if src == frozenset({1}) and dest == frozenset({2, 3})
    }


# fig:def:finite_automaton
def test_determinize_aabn(aabn: FiniteAutomatonFixture) -> None:
    det = determinize(aabn.aut)
    assert det.is_deterministic()
    aabn.assert_equivalent(det)


# ex:def:formal_language/leucine
def test_determinize_leucine(leucine: FiniteAutomatonFixture) -> None:
    det = determinize(leucine.aut)
    assert det.is_deterministic()
    assert frozenset({3, 6}) in det.get_states()
    leucine.assert_equivalent(det)
