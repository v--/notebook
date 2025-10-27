from collections.abc import Iterable, MutableSet, Sequence
from typing import NamedTuple, overload

from ...support.collections.sequential_set import SequentialSet


class FiniteAutomatonTransition[StateT, SymbolT](NamedTuple):
    src: StateT
    dest: StateT
    symbol: SymbolT


class FiniteAutomaton[StateT, SymbolT]:
    transitions: MutableSet[FiniteAutomatonTransition]
    initial: MutableSet[StateT]
    terminal: MutableSet[StateT]

    def __init__(
        self, *,
        transitions: Iterable[FiniteAutomatonTransition[StateT, SymbolT] | tuple[StateT, StateT, SymbolT]] | None = None,
        initial: Iterable[StateT] | None = None,
        terminal: Iterable[StateT] | None = None
    ) -> None:
        self.transitions = SequentialSet()
        self.initial = SequentialSet(initial) if initial else SequentialSet()
        self.terminal = SequentialSet(terminal) if terminal else SequentialSet()

        if transitions:
            for transition in transitions:
                self._add_transition_entire(transition)

    def _add_transition_entire(self, transition: FiniteAutomatonTransition | tuple[StateT, StateT, SymbolT]) -> None:
        if isinstance(transition, FiniteAutomatonTransition):
            self.transitions.add(transition)
        else:
            self.transitions.add(FiniteAutomatonTransition(*transition))

    def _add_transition_components(self, src: StateT, dest: StateT, symbol: SymbolT) -> None:
        self.transitions.add(FiniteAutomatonTransition(src, dest, symbol))

    @overload
    def add_transition(self, src: StateT, dest: StateT, symbol: SymbolT) -> None: ...
    @overload
    def add_transition(self, transition: FiniteAutomatonTransition | tuple[StateT, StateT, SymbolT]) -> None: ...
    def add_transition(self, *args, **kwargs) -> None:
        if len(args) + len(kwargs) == 1:
            self._add_transition_entire(*args, **kwargs)
        else:
            self._add_transition_components(*args, **kwargs)

    def _recognize_recurse(self, string: str, initial: StateT) -> bool:
        if len(string) == 0:
            return initial in self.terminal

        return any(
            self._recognize_recurse(string[1:], dest)
            for src, dest, symbol in self.transitions
            if src == initial and symbol == string[0]
        )

    def recognize(self, string: str) -> bool:
        return any(self._recognize_recurse(string, i) for i in self.initial)

    def get_states(self) -> Sequence[StateT]:
        result = SequentialSet[StateT]()

        for src, dest, _ in self.transitions:
            result.add(src)
            result.add(dest)

        return list(result)


def reverse_automaton[StateT, SymbolT](aut: FiniteAutomaton[StateT, SymbolT]) -> FiniteAutomaton[StateT, SymbolT]:
    return FiniteAutomaton(
        initial=aut.terminal,
        terminal=aut.initial,
        transitions=[(dest, src, symbol) for (src, dest, symbol) in aut.transitions]
    )
