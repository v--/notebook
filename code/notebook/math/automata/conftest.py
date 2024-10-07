from collections.abc import Iterable, Sequence
from typing import NamedTuple

import pytest

from .finite import FiniteAutomaton


class FiniteAutomatonFixture(NamedTuple):
    aut: FiniteAutomaton
    whitelist: Sequence[str]
    blacklist: Sequence[str]

    def assert_equivalent(self, other: FiniteAutomaton) -> None:
        for string in self.whitelist:
            assert other.recognize(string)

        for string in self.blacklist:
            assert not other.recognize(string)


@pytest.fixture
def aabn() -> FiniteAutomatonFixture:
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

    return FiniteAutomatonFixture(
        aut=aut,
        whitelist=['a', 'b', 'bb', 'bbb', 'bbbbbbbbbbbb'],
        blacklist=['', 'ab', 'abb', 'ba']
    )


@pytest.fixture
def leucine() -> FiniteAutomatonFixture:
    aut: FiniteAutomaton = FiniteAutomaton()
    aut.add_transition(1, 'C', 2)
    aut.add_transition(2, 'T', 3)
    aut.add_transition(3, 'C', 4)
    aut.add_transition(3, 'T', 5)
    aut.add_transition(2, 'T', 6)
    aut.add_transition(1, 'T', 7)
    aut.add_transition(6, 'A', 5)
    aut.add_transition(7, 'T', 6)
    aut.add_transition(6, 'G', 8)

    aut.initial.add(1)
    aut.terminal.add(4)
    aut.terminal.add(5)
    aut.terminal.add(8)

    return FiniteAutomatonFixture(
        aut=aut,
        whitelist=['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'],
        blacklist=['', 'T', 'TT', 'TTT', 'TTAT']
    )
