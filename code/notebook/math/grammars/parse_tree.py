from collections.abc import Iterable, Sequence
from typing import NamedTuple

from .alphabet import NonTerminal, Terminal
from .grammar import GrammarRule


class DerivationStep(NamedTuple):
    payload: Sequence[NonTerminal | Terminal]
    rule: GrammarRule


class Derivation(NamedTuple):
    start: NonTerminal
    steps: Sequence[DerivationStep]

    def __str__(self) -> str:
        return str(self.start) + ' ⟹ ' + ' ⟹ '.join(
            str(' '.join(str(s) for s in step.payload)) for step in self.steps
        )


class ParseTree(NamedTuple):
    payload: NonTerminal | Terminal
    subtrees: Sequence['ParseTree'] = []

    def is_leaf(self) -> bool:
        return len(self.subtrees) == 0

    def insert_subtree(self) -> None:
        pass

    def iter_symbols(self) -> Iterable[Terminal | NonTerminal]:
        yield self.payload

        for node in self.subtrees:
            yield from node.iter_symbols()

    def yield_string(self) -> str:
        return ''.join(sym.value for sym in self.iter_symbols() if isinstance(sym, Terminal))

    def __hash__(self) -> int:
        return hash(self.payload) ^ hash(tuple(self.subtrees))


def _insert_subtree_leftmost(tree: ParseTree, new_subtree: ParseTree) -> ParseTree | None:
    subtrees = list(tree.subtrees)

    for i, subtree in enumerate(tree.subtrees):
        if subtree.payload == new_subtree.payload and subtree.is_leaf():
            subtrees[i] = new_subtree
            break

        inserted = _insert_subtree_leftmost(subtree, new_subtree)

        if inserted is not None:
            subtrees[i] = inserted
            break
    else:
        return None

    return ParseTree(payload=tree.payload, subtrees=subtrees)


# This is alg:parse_tree_to_leftmost_derivation in the monograph
def derivation_to_parse_tree(derivation: Derivation) -> ParseTree:
    tree: ParseTree | None = None

    for step in derivation.steps:
        new_subtree = ParseTree(
            step.rule.src_symbol,
            [ParseTree(sym) for sym in step.rule.dest]
        )

        tree = new_subtree if tree is None else _insert_subtree_leftmost(tree, new_subtree)

    assert tree is not None
    return tree


def _iter_leftmost_parse_subtrees(tree: ParseTree) -> Iterable[ParseTree]:
    yield tree

    for subtree in tree.subtrees:
        if isinstance(subtree.payload, NonTerminal):
            yield from _iter_leftmost_parse_subtrees(subtree)


def _iter_leftmost_derivation_steps(tree: ParseTree) -> Iterable[DerivationStep]:
    last_step: DerivationStep | None = None

    for subtree in _iter_leftmost_parse_subtrees(tree):
        assert isinstance(subtree.payload, NonTerminal)
        rule = GrammarRule(
            [subtree.payload],
            [sstree.payload for sstree in subtree.subtrees]
        )

        if last_step is None:
            new_step_payload = rule.dest
        else:
            index = last_step.payload.index(subtree.payload)
            new_step_payload = [
                *last_step.payload[:index],
                *rule.dest,
                *last_step.payload[index + 1:]
            ]

        last_step = DerivationStep(new_step_payload, rule)
        yield last_step


# This is alg:derivation_to_parse_tree in the monograph
def parse_tree_to_derivation(tree: ParseTree) -> Derivation:
    assert isinstance(tree.payload, NonTerminal)
    return Derivation(tree.payload, list(_iter_leftmost_derivation_steps(tree)))
