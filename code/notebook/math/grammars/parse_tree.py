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
    children: list['ParseTree'] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def insert_subtree(self) -> None:
        pass

    def iter_symbols(self) -> Iterable[Terminal | NonTerminal | Empty]:
        yield self.payload

        for node in self.children:
            yield from node.iter_symbols()

    def yield_string(self) -> str:
        return ''.join(sym.value for sym in self.iter_symbols() if isinstance(sym, Terminal))

    def __hash__(self) -> int:
        return hash(self.payload) + functools.reduce(operator.xor, map(hash, self.children), 0)


def _insert_subtree_leftmost(tree: ParseTree, subtree: ParseTree) -> bool:
    for i, child in enumerate(tree.children):
        if child.payload == subtree.payload and child.is_leaf():
            tree.children[i] = subtree
            return True

    return any(_insert_subtree_leftmost(child, subtree) for child in tree.children)


# This is alg:parse_tree_to_leftmost_derivation in the text
def derivation_to_parse_tree(derivation: Derivation) -> ParseTree:
    tree = None

    for step in derivation.steps:
        subtree = ParseTree(step.rule.src_symbol)

        if is_epsilon_rule(step.rule):
            subtree.children.append(ParseTree(empty))
        else:
            subtree.children = [ParseTree(sym) for sym in step.rule.dest]

        if tree is None:
            tree = subtree
        else:
            assert _insert_subtree_leftmost(tree, subtree)

    return cast(ParseTree, tree)


# This is alg:derivation_to_parse_tree in the text
def parse_tree_to_derivation(tree: ParseTree) -> Derivation:
    assert isinstance(tree.payload, NonTerminal)
    queue: SimpleQueue[ParseTree] = SimpleQueue()

    first_rule = GrammarRule(
        [tree.payload],
        [subtree.payload for subtree in tree.children if isinstance(subtree.payload, Terminal | NonTerminal)]
    )

    derivation = Derivation(
        tree.payload,
        [
            DerivationStep(first_rule.dest, first_rule)
        ]
    )

    for subtree in tree.children:
        if isinstance(subtree.payload, NonTerminal):
            queue.put(subtree)

    while not queue.empty():
        subtree = queue.get()
        assert isinstance(subtree.payload, NonTerminal)
        last_step = derivation.steps[-1]
        index = last_step.payload.index(subtree.payload)
        new_step_payload = last_step.payload[:index] + \
            [subsubtree.payload for subsubtree in subtree.children if isinstance(subsubtree.payload, (Terminal, NonTerminal))] + \
            last_step.payload[index + 1:]

        new_step = DerivationStep(
            new_step_payload,
            GrammarRule(
                [subtree.payload],
                [subsubtree.payload for subsubtree in subtree.children if isinstance(subsubtree.payload, Terminal | NonTerminal)]
            )
        )

        derivation.steps.append(new_step)

        for subsubtree in subtree.children:
            if isinstance(subsubtree.payload, NonTerminal):
                queue.put(subsubtree)

    return derivation
