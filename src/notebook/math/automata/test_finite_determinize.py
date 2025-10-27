from .conftest import FiniteAutomatonFixture
from .finite import FiniteAutomaton
from .finite_determinize import determinize, is_automata_deterministic


# fig:def:finite_automaton
def test_determinize_preserves_parallel_arcs() -> None:
    aut: FiniteAutomaton = FiniteAutomaton()
    aut.add_transition(src=1, dest=2, symbol='a')
    aut.add_transition(src=1, dest=2, symbol='b')
    aut.add_transition(src=1, dest=3, symbol='a')
    aut.add_transition(src=1, dest=3, symbol='b')
    aut.add_transition(src=2, dest=3, symbol='b')
    aut.initial.add(1)
    aut.terminal.add(3)

    det = determinize(aut)

    assert {'a', 'b'} == {
        label
        for src, dest, label in det.transitions
        if set(src) == {1} and set(dest) == {2, 3}
    }


# fig:def:finite_automaton
def test_determinize_aabn(aabn: FiniteAutomatonFixture) -> None:
    det = determinize(aabn.aut)
    assert is_automata_deterministic(det)
    aabn.assert_equivalent(det)


# ex:def:formal_language/leucine
def test_determinize_leucine(leucine: FiniteAutomatonFixture) -> None:
    det = determinize(leucine.aut)
    assert is_automata_deterministic(det)
    assert {3, 6} in [set(state) for state in det.get_states()]
    leucine.assert_equivalent(det)
