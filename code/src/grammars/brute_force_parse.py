import itertools
from typing import Iterator

from .alphabet import NonTerminal, Terminal, empty
from .grammar import Grammar
from .context_free import is_context_free
from .parse_tree import ParseTree
from .epsilon_rules import is_epsilon_rule


def iter_partitions(seq: str, m: int) -> Iterator[list[str]]:
    if m == 1:
        yield [seq]
    else:
        for i in range(len(seq) + 1):
            for part in iter_partitions(seq[i:], m - 1):
                yield [seq[:i], *part]


def generate_trees(sym: NonTerminal | Terminal, string: str, grammar: Grammar, traversed: set[tuple[NonTerminal, str]]) -> Iterator[ParseTree]:
    if isinstance(sym, Terminal) and sym.value == string:
        yield ParseTree(sym)

    elif isinstance(sym, NonTerminal) and (sym, string) not in traversed:
        yield from parse(
            grammar.schema.instantiate(sym),
            string,
            {(grammar.start, string), *traversed}
        )


# This is alg:brute_force_parsing in the text
def parse(grammar: Grammar, string: str, traversed: set[tuple[NonTerminal, str]] = set()) -> Iterator[ParseTree]:
    assert is_context_free(grammar), 'Brute force parsing algorithm only works on context-free grammars'
    for rule in grammar.iter_starting_rules():
        if is_epsilon_rule(rule):
            if len(string) == 0:
                yield ParseTree(
                    rule.src_symbol,
                    [ParseTree(empty)]
                )
        else:
            for part in iter_partitions(string, len(rule.dest)):
                for subtrees in itertools.product(
                    *(
                        list(generate_trees(sym, substr, grammar, traversed))
                        for sym, substr in zip(rule.dest, part)
                    )
                ):
                    yield ParseTree(grammar.start, list(subtrees))


def derives(grammar: Grammar, string: str):
    return sum(1 for tree in parse(grammar, string)) > 0
