import itertools
from collections.abc import Iterator

from .alphabet import NonTerminal, Terminal
from .context_free import is_context_free
from .epsilon_rules import is_epsilon_rule
from .grammar import Grammar
from .parse_tree import ParseTree


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


# This is alg:brute_force_parsing in the monograph
def parse(grammar: Grammar, string: str, traversed: set[tuple[NonTerminal, str]] | None = None) -> Iterator[ParseTree]:
    if traversed is None:
        traversed = set()
    assert is_context_free(grammar), 'Brute force parsing algorithm only works on context-free grammars'
    for rule in grammar.iter_starting_rules():
        if is_epsilon_rule(rule):
            if len(string) == 0:
                yield ParseTree(rule.src_symbol, [])
        else:
            for part in iter_partitions(string, len(rule.dest)):
                for subtrees in itertools.product(
                    *(
                        list(generate_trees(sym, substr, grammar, traversed))
                        for sym, substr in zip(rule.dest, part, strict=True)
                    )
                ):
                    yield ParseTree(grammar.start, list(subtrees))


def derives(grammar: Grammar, string: str) -> bool:
    for _tree in parse(grammar, string):
        return True

    return False
