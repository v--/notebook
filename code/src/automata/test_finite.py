import pytest

from .finite import FiniteAutomaton, determinize


@pytest.fixture
def aabn():
    aut = FiniteAutomaton()
    aut.add_transition(1, 'a', 2)
    aut.add_transition(1, 'b', 3)
    aut.add_transition(1, 'a', 4)
    aut.add_transition(3, 'b', 3)
    aut.add_transition(4, 'a', 3)
    aut.add_transition(3, 'b', 5)

    aut.initial.add(1)
    aut.initial.add(3)
    aut.terminal.add(2)
    aut.terminal.add(5)

    return aut


def assert_aabn(aut: FiniteAutomaton):
    assert not aut.recognize('')
    assert not aut.recognize('ab')
    assert not aut.recognize('abb')
    assert not aut.recognize('ba')

    assert aut.recognize('a')
    assert aut.recognize('b')
    assert aut.recognize('bb')
    assert aut.recognize('bbb')
    assert aut.recognize('bbbbbbbbbbbb')
    assert aut.recognize('aab')


@pytest.fixture
def leucine():
    aut = FiniteAutomaton()
    aut.add_transition(1, 'C', 2)
    aut.add_transition(2, 'U', 3)
    aut.add_transition(3, 'C', 4)
    aut.add_transition(3, 'U', 5)
    aut.add_transition(2, 'U', 6)
    aut.add_transition(1, 'U', 7)
    aut.add_transition(6, 'A', 5)
    aut.add_transition(7, 'U', 6)
    aut.add_transition(6, 'G', 8)

    aut.initial.add(1)
    aut.terminal.add(4)
    aut.terminal.add(5)
    aut.terminal.add(8)

    return aut


def assert_leucine(aut: FiniteAutomaton):
    assert not aut.recognize('')
    assert not aut.recognize('U')
    assert not aut.recognize('UU')
    assert not aut.recognize('UUU')
    assert not aut.recognize('UUAU')

    assert aut.recognize('UUA')
    assert aut.recognize('UUG')
    assert aut.recognize('CUU')
    assert aut.recognize('CUC')
    assert aut.recognize('CUA')
    assert aut.recognize('CUG')


# ex:def:formal_language/an
def test_finite_automaton_recognizes_an():
    aut = FiniteAutomaton()
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


# fig:def:finite_automaton
def test_determinize_preserves_parallel_arcs():
    aut = FiniteAutomaton()
    aut.add_transition(1, 'a', 2)
    aut.add_transition(1, 'b', 2)
    aut.add_transition(1, 'a', 3)
    aut.add_transition(1, 'b', 3)
    aut.add_transition(2, 'b', 3)
    aut.initial.add(1)
    aut.terminal.add(3)

    det = determinize(aut)

    assert {'a', 'b'} == set(
        label
        for src, label, dest in det.triples
        if src == frozenset({1}) and dest == frozenset({2, 3})
    )


# fig:def:finite_automaton
def test_determinize_aabn(aabn: FiniteAutomaton):
    det = determinize(aabn)
    assert det.is_deterministic()
    assert_aabn(det)


# ex:def:formal_language/leucine
def test_determinize_leucine(leucine: FiniteAutomaton):
    det = determinize(leucine)
    assert det.is_deterministic()
    assert frozenset({3, 6}) in det.get_states()
    assert_leucine(det)
