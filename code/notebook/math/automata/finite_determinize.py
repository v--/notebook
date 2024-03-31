import itertools

from .finite import FiniteAutomaton, FiniteAutomatonTransition, LabelT, StateT


def determinize_recurse(
    nondet: FiniteAutomaton[StateT, LabelT],
    visited: set[frozenset[StateT]],
    src_set: frozenset[StateT]
) -> list[FiniteAutomatonTransition[frozenset[StateT], LabelT]]:
    by_label: dict[LabelT, set[StateT]] = {}
    triples: list[FiniteAutomatonTransition[frozenset[StateT], LabelT]] = []

    for src, label, dest in nondet.triples:
        if src in src_set:
            by_label[label] = by_label.get(label, set())
            by_label[label].add(dest)

    for label, dest_set_mut in by_label.items():
        dest_set = frozenset(dest_set_mut)
        triples.append((src_set, label, dest_set))

    return list(
        set(
            itertools.chain(
                triples,
                *(
                    determinize_recurse(nondet, visited | {src_set}, frozenset(dest_set_mut))
                    for dest_set_mut in by_label.values()
                    if frozenset(dest_set_mut) not in visited
                )
            )
        )
    )


def determinize(nondet: FiniteAutomaton[StateT, LabelT]) -> FiniteAutomaton[frozenset[StateT], LabelT]:
    triples = determinize_recurse(
        nondet,
        set(),
        frozenset(nondet.initial)
    )

    return FiniteAutomaton(
        triples,
        initial={frozenset(nondet.initial)},
        terminal=(
            set(src for src, _, _ in triples if len(src & nondet.terminal) > 0) |
            set(dest for _, _, dest in triples if len(dest & nondet.terminal) > 0)
        ),
    )
