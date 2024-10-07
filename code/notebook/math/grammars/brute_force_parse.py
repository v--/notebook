import itertools
from collections.abc import Iterable, Sequence

from .alphabet import NonTerminal, Terminal
from .context_free import is_context_free
from .epsilon_rules import is_epsilon_rule
from .exceptions import GrammarError
from .grammar import Grammar
from .parse_tree import ParseTree


class BruteForceParseError(GrammarError):
    pass


class NoParseTreeError(BruteForceParseError):
    pass


def iter_partitions(seq: str, m: int) -> Iterable[Sequence[str]]:
    if m == 1:
        yield [seq]
    else:
        for i in range(len(seq) + 1):
            for part in iter_partitions(seq[i:], m - 1):
                yield [seq[:i], *part]


def generate_trees(sym: NonTerminal | Terminal, string: str, grammar: Grammar, traversed: set[tuple[NonTerminal, str]]) -> Iterable[ParseTree]:
    if isinstance(sym, Terminal) and sym.value == string:
        yield ParseTree(sym)

    elif isinstance(sym, NonTerminal) and (sym, string) not in traversed:
        yield from parse_impl(
            grammar.schema.instantiate(sym),
            string,
            {(grammar.start, string), *traversed}
        )


def parse_impl(grammar: Grammar, string: str, traversed: set[tuple[NonTerminal, str]]) -> Iterable[ParseTree]:
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


# This is alg:brute_force_parsing in the monograph
def parse(grammar: Grammar, string: str) -> Iterable[ParseTree]:
    trees = list(parse_impl(grammar, string, set()))

    if len(trees) == 0:
        raise NoParseTreeError(f'No parse trees generated for {string!r}')

    return trees


def derives(grammar: Grammar, string: str) -> bool:
    try:
        for _ in parse(grammar, string):
            pass
    except NoParseTreeError:
        return False
    else:
        return True
