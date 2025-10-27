import itertools
from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass, field

from ...support.iteration import string_accumulator
from .alphabet import NonTerminal, Terminal, empty
from .exceptions import GrammarError, UnknownSymbolError


@dataclass(frozen=True)
class GrammarRule:
    src: Sequence[Terminal | NonTerminal]
    dest: Sequence[Terminal | NonTerminal]

    @property
    def src_symbol(self) -> NonTerminal:
        if len(self.src) != 1:
            raise GrammarError('Only context-free rules have a source symbol')

        value = self.src[0]
        assert isinstance(value, NonTerminal)
        return value

    @string_accumulator()
    def __str__(self) -> Iterable[str]:  # noqa: PLE0307
        for sym in self.src:
            yield str(sym)
            yield ' '

        yield '→'

        if len(self.dest) == 0:
            yield ' '
            yield empty
        else:
            for sym in self.dest:
                yield ' '
                yield str(sym)

    def __hash__(self) -> int:
        return hash(str(self))

    def get_terminals(self) -> Collection[Terminal]:
        return {
            sym for sym in itertools.chain(self.src, self.dest) if isinstance(sym, Terminal)
        }

    def get_non_terminals(self) -> Collection[NonTerminal]:
        return {
            sym for sym in itertools.chain(self.src, self.dest) if isinstance(sym, NonTerminal)
        }


@dataclass(frozen=True)
class GrammarSchema:
    rules: Sequence[GrammarRule] = field(default_factory=list)

    def __str__(self) -> str:
        return '\n'.join(str(rule) for rule in self.rules) + '\n'

    def get_terminals(self) -> Collection[Terminal]:
        result = set[Terminal]()

        for rule in self.rules:
            for symbol in rule.get_terminals():
                result.add(symbol)

        return result

    def get_non_terminals(self) -> Collection[NonTerminal]:
        result = set[NonTerminal]()

        for rule in self.rules:
            for symbol in rule.get_non_terminals():
                result.add(symbol)

        return result

    def instantiate(self, start: NonTerminal) -> 'Grammar':
        return Grammar(self, start)


@dataclass(frozen=True)
class Grammar:
    schema: GrammarSchema
    start: NonTerminal

    def __post_init__(self) -> None:
        if self.start not in self.schema.get_non_terminals():
            raise UnknownSymbolError(f'The grammar schema does not contain {self.start}')

    def iter_starting_rules(self) -> Iterable[GrammarRule]:
        for rule in self.schema.rules:
            if rule.src == [self.start]:
                yield rule
