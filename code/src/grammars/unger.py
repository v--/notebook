from __future__ import annotations
import itertools
from typing import Iterator

from .grammar import SingletonSymbol, epsilon, Grammar, NonTerminal, Terminal
from .context_free import is_context_free
from .parse_tree import ParseTree
from .epsilon_rules import is_epsilon_rule


def iter_partitions(seq: str, n: int) -> Iterator[list[str]]:
    if n == 1:
        yield [seq]
    else:
        for i in range(len(seq) + 1):
            for part in iter_partitions(seq[i:], n - 1):
                yield [seq[:i], *part]


def generate_trees(sym: NonTerminal | Terminal | SingletonSymbol, string: str, grammar: Grammar, used: set[tuple[NonTerminal, str]] = set()) -> list[ParseTree]:
    if isinstance(sym, Terminal) and sym.value == string:
        return [ParseTree(sym)]

    if isinstance(sym, NonTerminal) and (sym, string) not in used:
        return list(
            parse(
                grammar.schema.instantiate(sym),
                string,
                {(grammar.start, string), *used}
            )
        )

    return []


def parse(grammar: Grammar, string: str, used: set[tuple[NonTerminal, str]] = set()) -> Iterator[ParseTree]:
    assert is_context_free(grammar), "Unger's parsing algorithm only works on context-free grammars"
    for rule in grammar.iter_starting_rules():
        if is_epsilon_rule(rule):
            if len(string) == 0:
                yield ParseTree(
                    rule.src_symbol,
                    [ParseTree(epsilon)]
                )
        else:
            for part in iter_partitions(string, len(rule.dest)):
                for subtrees in itertools.product(
                    *(
                        generate_trees(sym, substr, grammar, used)
                        for sym, substr in zip(rule.dest, part)
                    )
                ):
                    yield ParseTree(grammar.start, list(subtrees))


def derives(grammar: Grammar, string: str):
    return sum(1 for tree in parse(grammar, string)) > 0
