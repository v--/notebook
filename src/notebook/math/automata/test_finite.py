from typing import TYPE_CHECKING

from notebook.support.coderefs import collector

from .finite import FiniteAutomaton


if TYPE_CHECKING:
    from .conftest import FiniteAutomatonFixture


@collector.ref('ex:def:formal_language/an')
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
