from __future__ import annotations
from typing import Iterator

from .grammar import Epsilon, Grammar, NonTerminal, Terminal
from .chomsky import is_context_free
from .parse_tree import ParseTree


def iter_partitions(seq: str, n: int) -> Iterator[list[str]]:
    if n == 1:
        yield [seq]
    else:
        for i in range(len(seq) + 1):
            for part in iter_partitions(seq[i:], n - 1):
                yield [seq[:i], *part]


def parse(grammar: Grammar, string: str, used: set[tuple[NonTerminal, str]] = set()) -> ParseTree | None:
    assert is_context_free(grammar), 'Unger parsing only works on context-free grammars'

    for rule in grammar.iter_starting_rules():
        for part in iter_partitions(string, len(rule.dest)):
            tree = ParseTree(grammar.start)

            for sym, substr in zip(rule.dest, part):
                if isinstance(sym, Epsilon):
                    if len(substr) == 0:
                        tree.successors.append(ParseTree(sym))
                    else:
                        break

                if isinstance(sym, Terminal):
                    if sym.value == substr:
                        tree.successors.append(ParseTree(sym))
                    else:
                        break

                if isinstance(sym, NonTerminal):
                    if (sym, substr) in used:
                        break

                    subtree = parse(
                        grammar.schema.instantiate(sym),
                        substr,
                        {(sym, substr), *used}
                    )

                    if subtree is None:
                        break
                    else:
                        tree.successors.append(subtree)
            else:
                return tree

    return None
