from __future__ import annotations
import itertools
from typing import Iterator

from .grammar import SingletonSymbol, epsilon, Grammar, NonTerminal, Terminal
from .chomsky import is_context_free
from .parse_tree import ParseTree


def iter_partitions(seq: str, dest: list[NonTerminal | Terminal | SingletonSymbol]) -> Iterator[list[str]]:
    if len(seq) == 0:
        pass
    elif len(dest) == 1:
        yield [seq]
    else:
        head = dest[0]
        tail = dest[1:]

        if head == epsilon:
            for part in iter_partitions(seq, tail):
                yield ['', *part]
        elif isinstance(head, Terminal) and seq[0] == head.value:
            for part in iter_partitions(seq[1:], tail):
                yield [seq[0], *part]
        elif isinstance(head, NonTerminal):
            for i in range(len(seq) + 1):
                for part in iter_partitions(seq[i:], tail):
                    yield [seq[:i], *part]


def generate_trees(sym: NonTerminal | Terminal | SingletonSymbol, string: str, grammar: Grammar, used: set[tuple[NonTerminal, str]] = set()) -> list[ParseTree]:
    if isinstance(sym, Terminal) and sym.value == string:
        return [ParseTree(sym)]

    if isinstance(sym, NonTerminal) and (sym, string) not in used:
        return list(
            parse_impl(
                grammar.schema.instantiate(sym),
                string,
                {(grammar.start, string), *used}
            )
        )

    return []


def parse_impl(grammar: Grammar, string: str, used: set[tuple[NonTerminal, str]]) -> Iterator[ParseTree]:
    for rule in grammar.iter_starting_rules():
        if rule.dest == [epsilon] and len(string) == 0:
            yield ParseTree(
                rule.src[0],
                [ParseTree(epsilon)]
            )
        else:
            for part in iter_partitions(string, rule.dest):
                for subtrees in itertools.product(
                    *(
                        generate_trees(sym, substr, grammar, used) for sym, substr in zip(rule.dest, part)
                    )
                ):
                    yield ParseTree(grammar.start, list(subtrees))


def parse(grammar: Grammar, string: str) -> Iterator[ParseTree]:
    assert is_context_free(grammar), "Unger's parsing algorithm only works on context-free grammars"
    return parse_impl(grammar, string, set())
