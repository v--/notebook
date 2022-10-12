from __future__ import annotations

from dataclasses import dataclass, field
import functools
import operator
from typing import Any, cast
import itertools
from parsimonious.exceptions import ParseError

from rich.tree import Tree
from rich.console import Console

from ..support.rich import rich_to_text

from .grammar import GrammarRule, SingletonSymbol, epsilon, NonTerminal, Terminal


@dataclass
class DerivationStep:
    payload: list[NonTerminal | Terminal]
    rule: GrammarRule


@dataclass
class Derivation:
    start: NonTerminal
    steps: list[DerivationStep]


@dataclass
class ParseTree:
    _rich_console = Console(record=True)
    payload: Terminal | NonTerminal | SingletonSymbol
    children: list[ParseTree] = field(default_factory=list)

    def is_leaf(self):
        return len(self.children) == 0

    def insert_subtree(self):
        pass

    def iter_symbols(self):
        yield self.payload

        for node in self.children:
            yield from node.iter_symbols()

    def yield_word(self):
        return ''.join(sym.value for sym in self.iter_symbols() if isinstance(sym, Terminal))

    def build_rich_tree(self):
        if self.payload == epsilon:
            tree = Tree('ε')
        else:
            tree = Tree(str(self.payload))

        for node in self.children:
            tree.add(node.build_rich_tree())

        return tree

    def __str__(self):
        return rich_to_text(self.build_rich_tree())

    def __hash__(self):
        return hash(self.payload) + functools.reduce(operator.xor, map(hash, self.children), 0)


class RuleVisitor:
    def visit(self, tree: ParseTree):
        if isinstance(tree.payload, NonTerminal):
            args = [self.visit(succ) for succ in tree.children]
            return getattr(self, 'visit_' + tree.payload.value, self.generic_visit)(tree, *args)

        if isinstance(tree.payload, Terminal):
            return tree.payload.value

        # We do nothing on epsilon rules

    def generic_visit(self, tree: ParseTree, *args: Any):
        pass


def _insert_subtree_leftmost(tree: ParseTree, subtree: ParseTree):
    for i, child in enumerate(tree.children):
        if child.payload == subtree.payload and child.is_leaf():
            tree.children[i] = subtree
            return True
    else:
        for child in tree.children:
            if _insert_subtree_leftmost(child, subtree):
                return True

    return False


def derivation_to_parse_tree(derivation: Derivation) -> ParseTree:
    tree = None

    for step in derivation.steps:
        subtree = ParseTree(step.rule.src[0])

        if len(step.rule.dest) == 0:
            subtree.children.append(ParseTree(epsilon))
        else:
            for sym in step.rule.dest:
                subtree.children.append(ParseTree(sym))

        if tree is None:
            tree = subtree
        else:
            assert _insert_subtree_leftmost(tree, subtree)

    return cast(ParseTree, tree)
