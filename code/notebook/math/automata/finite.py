from dataclasses import dataclass, field
from typing import Generic, TypeVar


StateT = TypeVar('StateT')
LabelT = TypeVar('LabelT')


FiniteAutomatonTransition = tuple[StateT, LabelT, StateT]


@dataclass
class FiniteAutomaton(Generic[StateT, LabelT]):
    triples: list[FiniteAutomatonTransition] = field(default_factory=list)
    initial: set[StateT] = field(default_factory=set)
    terminal: set[StateT] = field(default_factory=set)

    def add_transition(self, src: StateT, label: LabelT, dest: StateT) -> None:
        self.triples.append((src, label, dest))

    def _recognize_recurse(self, string: str, initial: StateT) -> bool:
        if len(string) == 0:
            return initial in self.terminal

        return any(
            self._recognize_recurse(string[1:], dest)
            for src, label, dest in self.triples
            if src == initial and label == string[0]
        )

    def recognize(self, string: str) -> bool:
        return any(self._recognize_recurse(string, i) for i in self.initial)

    def is_deterministic(self) -> bool:
        if len(self.initial) != 1:
            return False

        used_labels: dict[StateT, set[LabelT]] = {}

        for src, label, _ in self.triples:
            used_labels[src] = used_labels.get(src, set())

            if label in used_labels[src]:
                return False

            used_labels[src].add(label)

        return True

    def get_states(self) -> list[StateT]:
        return [src for src, _, _ in self.triples] + [dest for dest, _, _ in self.triples]

    def __str__(self) -> str:
        transition_str = '\n\t'.join(f'{src} -{label}-> {dest}' for src, label, dest in self.triples)
        return f'Initial: \n\t{self.initial!s}\nTerminal: \n\t{self.terminal!s}\nTransitions: \n\t{transition_str}'


def reverse_automaton(aut: FiniteAutomaton[StateT, LabelT]) -> FiniteAutomaton[StateT, LabelT]:
    return FiniteAutomaton(
        triples=[(dest, label, src) for (src, label, dest) in aut.triples],
        initial=aut.terminal,
        terminal=aut.initial
    )
