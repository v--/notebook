import functools
import operator
from collections.abc import Iterable
from dataclasses import dataclass, field
from queue import SimpleQueue
from typing import cast

from .alphabet import Empty, NonTerminal, Terminal, empty
from .epsilon_rules import is_epsilon_rule
from .grammar import GrammarRule


@dataclass
class DerivationStep:
    payload: list[NonTerminal | Terminal]
    rule: GrammarRule


@dataclass
class Derivation:
    start: NonTerminal
    steps: list[DerivationStep]

    def __str__(self) -> str:
        return str(self.start) + ' ⟹ ' + ' ⟹ '.join(
            str(' '.join(str(s) for s in step.payload)) for step in self.steps
        )


@dataclass
class ParseTree:
    payload: NonTerminal | Terminal | Empty
    subtrees: list['ParseTree'] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return len(self.subtrees) == 0

    def insert_subtree(self) -> None:
        pass

    def iter_symbols(self) -> Iterable[Terminal | NonTerminal | Empty]:
        yield self.payload

        for node in self.subtrees:
            yield from node.iter_symbols()

    def yield_string(self) -> str:
        return ''.join(sym.value for sym in self.iter_symbols() if isinstance(sym, Terminal))

    def __hash__(self) -> int:
        return hash(self.payload) ^ hash(tuple(self.subtrees))


def _insert_subtree_leftmost(tree: ParseTree, subtree: ParseTree) -> bool:
    for i, child in enumerate(tree.subtrees):
        if child.payload == subtree.payload and child.is_leaf():
            tree.subtrees[i] = subtree
            return True

    return any(_insert_subtree_leftmost(child, subtree) for child in tree.subtrees)


# This is alg:parse_tree_to_leftmost_derivation in the monograph
def derivation_to_parse_tree(derivation: Derivation) -> ParseTree:
    tree = None

    for step in derivation.steps:
        subtree = ParseTree(step.rule.src_symbol)

        if is_epsilon_rule(step.rule):
            subtree.subtrees.append(ParseTree(empty))
        else:
            subtree.subtrees = [ParseTree(sym) for sym in step.rule.dest]

        if tree is None:
            tree = subtree
        else:
            assert _insert_subtree_leftmost(tree, subtree)

    return cast(ParseTree, tree)


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
            [sstree.payload for sstree in subtree.subtrees if isinstance(sstree.payload, Terminal | NonTerminal)]
        )

        if last_step is None:
            new_step_payload = rule.dest
        else:
            index = last_step.payload.index(subtree.payload)
            new_step_payload = last_step.payload[:index] + rule.dest + last_step.payload[index + 1:]

        last_step = DerivationStep(new_step_payload, rule)
        yield last_step


# This is alg:derivation_to_parse_tree in the monograph
def parse_tree_to_derivation(tree: ParseTree) -> Derivation:
    assert isinstance(tree.payload, NonTerminal)
    return Derivation(tree.payload, list(_iter_leftmost_derivation_steps(tree)))
