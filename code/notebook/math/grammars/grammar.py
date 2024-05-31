import functools
import itertools
from collections.abc import Iterable
from dataclasses import dataclass, field

from .alphabet import NonTerminal, Terminal, empty


@dataclass
class GrammarRule:
    src: list[Terminal | NonTerminal]
    dest: list[Terminal | NonTerminal]

    @property
    def src_symbol(self) -> NonTerminal:
        assert len(self.src) == 1
        assert isinstance(self.src[0], NonTerminal)
        return self.src[0]

    def __str__(self) -> str:
        return ' '.join(str(sym) for sym in self.src) + ' → ' + (' '.join(str(sym) for sym in self.dest) if len(self.dest) > 0 else empty)

    def __hash__(self) -> int:
        return hash(str(self))

    def get_terminals(self) -> frozenset[Terminal]:
        return frozenset(
            sym for sym in itertools.chain(self.src, self.dest) if isinstance(sym, Terminal)
        )

    def get_non_terminals(self) -> frozenset[NonTerminal]:
        return frozenset(
            sym for sym in itertools.chain(self.src, self.dest) if isinstance(sym, NonTerminal)
        )


@dataclass
class GrammarSchema:
    rules: list[GrammarRule] = field(default_factory=list)

    def __str__(self) -> str:
        return '\n'.join(str(rule) for rule in self.rules)

    def get_terminals(self) -> set[Terminal]:
        return functools.reduce(
            set.union,
            (set(rule.get_terminals()) for rule in self.rules)
        )

    def get_non_terminals(self) -> set[NonTerminal]:
        return functools.reduce(
            set.union,
            (set(rule.get_non_terminals()) for rule in self.rules)
        )

    def instantiate(self, start: NonTerminal) -> 'Grammar':
        assert start in self.get_non_terminals()
        return Grammar(self, start)


@dataclass
class Grammar:
    schema: GrammarSchema
    start: NonTerminal

    def __post_init__(self) -> None:
        assert self.start in self.schema.get_non_terminals(), f'The starting symbol {self.start} must be a nonterminal in {self.schema}'

    def iter_starting_rules(self) -> Iterable[GrammarRule]:
        for rule in self.schema.rules:
            if rule.src == [self.start]:
                yield rule
