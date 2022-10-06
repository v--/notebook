from __future__ import annotations

from dataclasses import dataclass, field

from rich.tree import Tree

from .grammar import Epsilon, NonTerminal, Terminal


@dataclass
class ParseTree:
    payload: Terminal | NonTerminal | Epsilon
    successors: list[ParseTree] = field(default_factory=list)

    def yield_word_iter(self):
        if isinstance(self.payload, Terminal):
            yield self.payload.value

        for node in self.successors:
            yield from node.yield_word()

    def yield_word(self):
        return ''.join(self.yield_word_iter())

    def build_rich_tree(self):
        if isinstance(self.payload, Epsilon):
            tree = Tree('ε')
        else:
            tree = Tree(self.payload.value)

        for node in self.successors:
            tree.add(node.build_rich_tree())

        return tree
