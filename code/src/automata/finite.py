from dataclasses import dataclass, field
from typing import Generic, TypeVar


TState = TypeVar('TState')
TLabel = TypeVar('TLabel')


FiniteAutomatonTransition = tuple[TState, TLabel, TState]


@dataclass
class FiniteAutomaton(Generic[TState, TLabel]):
    triples: list[FiniteAutomatonTransition] = field(default_factory=list)
    initial: set[TState] = field(default_factory=set)
    terminal: set[TState] = field(default_factory=set)

    def add_transition(self, src: TState, label: TLabel, dest: TState):
        self.triples.append((src, label, dest))

    def _recognize_recurse(self, word: str, initial: TState):
        if len(word) == 0:
            return initial in self.terminal

        return any(
            self._recognize_recurse(word[1:], dest)
            for src, label, dest in self.triples
            if src == initial and label == word[0]
        )

    def recognize(self, word: str):
        return any(self._recognize_recurse(word, i) for i in self.initial)

    def is_deterministic(self):
        if len(self.initial) != 1:
            return False

        used_labels: dict[TState, set[TLabel]] = {}

        for src, label, _ in self.triples:
            used_labels[src] = used_labels.get(src, set())

            if label in used_labels[src]:
                return False

            used_labels[src].add(label)

        return True

    def get_states(self):
        return [src for src, _, _ in self.triples] + [dest for dest, _, _ in self.triples]

    def __str__(self):
        transition_str = '\n\t'.join(f'{src} -{label}-> {dest}' for src, label, dest in self.triples)
        return f'Initial: \n\t{str(self.initial)}\nTerminal: \n\t{str(self.terminal)}\nTransitions: \n\t{transition_str}'


def reverse_automaton(aut: FiniteAutomaton[TState, TLabel]) -> FiniteAutomaton[TState, TLabel]:
    return FiniteAutomaton(
        triples=[(dest, label, src) for (src, label, dest) in aut.triples],
        initial=aut.terminal,
        terminal=aut.initial
    )
