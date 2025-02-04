from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import pytest

from .finite import FiniteAutomaton


@dataclass(frozen=True)
class FiniteAutomatonFixture:
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
    aut.add_transition(src=1, dest=2, symbol='a')
    aut.add_transition(src=1, dest=3, symbol='b')
    aut.add_transition(src=1, dest=4, symbol='a')
    aut.add_transition(src=3, dest=3, symbol='b')
    aut.add_transition(src=4, dest=3, symbol='a')
    aut.add_transition(src=3, dest=5, symbol='b')

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
    aut.add_transition(src=1, dest=2, symbol='C')
    aut.add_transition(src=2, dest=3, symbol='T')
    aut.add_transition(src=3, dest=4, symbol='C')
    aut.add_transition(src=3, dest=5, symbol='T')
    aut.add_transition(src=2, dest=6, symbol='T')
    aut.add_transition(src=1, dest=7, symbol='T')
    aut.add_transition(src=6, dest=5, symbol='A')
    aut.add_transition(src=7, dest=6, symbol='T')
    aut.add_transition(src=6, dest=8, symbol='G')

    aut.initial.add(1)
    aut.terminal.add(4)
    aut.terminal.add(5)
    aut.terminal.add(8)

    return FiniteAutomatonFixture(
        aut=aut,
        whitelist=['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'],
        blacklist=['', 'T', 'TT', 'TTT', 'TTAT']
    )
