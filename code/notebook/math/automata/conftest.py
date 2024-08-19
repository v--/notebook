import pytest

from .finite import FiniteAutomaton


@pytest.fixture
def aabn() -> FiniteAutomaton:
    aut: FiniteAutomaton = FiniteAutomaton()
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


def assert_aabn(aut: FiniteAutomaton) -> None:
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
def leucine() -> FiniteAutomaton:
    aut: FiniteAutomaton = FiniteAutomaton()
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


def assert_leucine(aut: FiniteAutomaton) -> None:
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
