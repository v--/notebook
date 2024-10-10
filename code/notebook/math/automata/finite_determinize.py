from collections.abc import Collection

from ...support.collections.sequential_mapping import SequentialMapping
from ...support.collections.sequential_set import SequentialSet
from .finite import FiniteAutomaton


def is_automata_deterministic[StateT, SymbolT](aut: FiniteAutomaton[StateT, SymbolT]) -> bool:
    if len(aut.initial) != 1:
        return False

    used_symbols = SequentialMapping[StateT, SequentialSet[SymbolT]]()

    for src, _, symbol in aut.transitions:
        used_symbols.setdefault(src, SequentialSet())

        if symbol in used_symbols[src]:
            return False

        used_symbols[src].add(symbol)

    return True


def _determinize_recurse[StateT, SymbolT](
    nondet: FiniteAutomaton[StateT, SymbolT],
    det: FiniteAutomaton[Collection[StateT], SymbolT],
    visited: Collection[Collection[StateT]],
    src_set: Collection[StateT],
) -> None:
    by_symbol = SequentialMapping[SymbolT, SequentialSet[StateT]]()

    for src, dest, symbol in nondet.transitions:
        if src in src_set:
            by_symbol.setdefault(symbol, SequentialSet())
            by_symbol[symbol].add(dest)

    for symbol, dest_set in by_symbol.items():
        det.add_transition(src_set, dest_set, symbol)

    new_visited = SequentialSet(visited)
    new_visited.add(src_set)

    for dest_set in by_symbol.values():
        if dest_set not in visited:
            _determinize_recurse(nondet, det, new_visited, dest_set)


def determinize[StateT, SymbolT](nondet: FiniteAutomaton[StateT, SymbolT]) -> FiniteAutomaton[Collection[StateT], SymbolT]:
    det = FiniteAutomaton[Collection[StateT], SymbolT]()
    det.initial.add(nondet.initial)

    _determinize_recurse(
        nondet,
        det,
        visited=SequentialSet(),
        src_set=nondet.initial
    )

    for src, dest, _ in det.transitions:
        if any(state in nondet.terminal for state in src):
            det.terminal.add(src)

        if any(state in nondet.terminal for state in dest):
            det.terminal.add(dest)

    return det
