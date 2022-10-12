from __future__ import annotations
from collections.abc import Sequence

from dataclasses import dataclass, field
import functools
import itertools

from ..support.parsing import Parser


@dataclass
class GrammarSymbol:
    value: str

    def __str__(self):
        return f'{self.value}'

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object):
        return isinstance(other, type(self)) and self.value == other.value


class SingletonSymbol(GrammarSymbol):
    pass


space = SingletonSymbol(' ')
epsilon = SingletonSymbol('ε')
right_arrow = SingletonSymbol('→')
pipe = SingletonSymbol('|')
new_line = SingletonSymbol('\n')


class Terminal(GrammarSymbol):
    def __str__(self):
        return f'"{self.value}"'


class NonTerminal(GrammarSymbol):
    def __str__(self):
        return f'<{self.value}>'


class GrammarTokenizer(Parser[str]):
    def parse_string(self, delim_a: str, delim_b: str):
        assert self.peek() == delim_a
        self.advance()
        buffer: list[str] = []

        while self.peek() != delim_b:
            if self.is_at_end():
                raise self.error(f'String not closed', precede=len(buffer) + 1)

            if self.peek() == delim_a:
                raise self.error(f'Strings cannot be nested', precede=len(buffer) + 1)

            if self.peek_multiple(2) in (r'\<', r'\>', r'\"', r'\\'):
                self.advance()
                buffer.append(*self.peek())
                self.advance()
            else:
                buffer.append(*self.peek())
                self.advance()

        self.advance()
        return ''.join(buffer)

    def parse(self):
        while not self.is_at_end():
            symbol = self.peek()

            if symbol == 'ε':
                yield epsilon
                self.advance()

            elif symbol == '→':
                yield right_arrow
                self.advance()

            elif symbol == '|':
                yield pipe
                self.advance()

            elif symbol == '\n':
                yield new_line
                self.advance()

            elif symbol == ' ':
                yield space
                self.advance()

            elif symbol == '<':
                yield NonTerminal(self.parse_string('<', '>'))

            elif symbol == '"':
                yield Terminal(self.parse_string('"', '"'))

            else:
                raise self.error(f'Unexpected symbol')


class GrammarParser(Parser[Sequence[GrammarSymbol]]):
    def parse(self):
        src: list[Terminal | NonTerminal] = []
        dest: list[Terminal | NonTerminal | SingletonSymbol] = []
        in_dest = False

        while not self.is_at_end():
            symbol = self.peek()

            if symbol == new_line or symbol == pipe:
                if in_dest and len(dest) > 0:
                    yield src, dest
                elif len(src) > 0:
                    raise self.error(f'Attempting to end an incomplete rule')

                if symbol == new_line:
                    src = []
                    in_dest = False

                dest = []
                self.advance()

            elif isinstance(symbol, (Terminal, NonTerminal)):
                if in_dest:
                    if epsilon in dest:
                        raise self.error(f'Unexpected {symbol} after ε')

                    dest.append(symbol)
                else:
                    src.append(symbol)

                self.advance()

            elif symbol == epsilon:
                if in_dest and len(dest) == 0:
                    dest.append(epsilon)
                else:
                    raise self.error(f'ε is only allowed on its own on the right side of a rule')

                self.advance()

            elif symbol == right_arrow:
                if in_dest:
                    raise self.error(f'Only one → allowed per line')

                in_dest = True
                self.advance()

            else:
                self.advance()


@dataclass
class GrammarRule:
    src: list[Terminal | NonTerminal]
    dest: list[Terminal | NonTerminal | SingletonSymbol]

    def __post_init__(self):
        assert any(isinstance(sym, NonTerminal) for sym in self.src), 'The source must contain at least one non-terminal, but it is {}'.format(' '.join(str(sym) for sym in self.src))
        assert all(sym != epsilon for sym in self.dest) or len(self.dest) == 1, 'epsilon rules cannot contain other symbols, got {}'.format(' '.join(str(sym) for sym in self.dest))

    @classmethod
    def parse(cls, string: str):
        tokens = list(GrammarTokenizer(string).parse())

        for src, dest in GrammarParser(tokens).parse():
            yield cls(src, dest)

    @property
    def is_epsilon(self):
        return self.dest == [epsilon]

    def __str__(self):
        return ' '.join(str(sym) for sym in self.src) + ' → ' + ' '.join(str(sym) for sym in self.dest)

    def __hash__(self):
        return hash(str(self))

    def get_terminals(self):
        return set(
            sym for sym in itertools.chain(self.src, self.dest) if isinstance(sym, Terminal)
        )

    def get_non_terminals(self):
        return set(
            sym for sym in itertools.chain(self.src, self.dest) if isinstance(sym, NonTerminal)
        )


@dataclass
class GrammarSchema:
    rules: list[GrammarRule] = field(default_factory=list)

    def __str__(self):
        return '\n'.join(str(rule) for rule in self.rules)

    @classmethod
    def parse(cls, string: str):
        return cls(list(GrammarRule.parse(string)))

    def get_terminals(self):
        return functools.reduce(
            set.union,
            (set(rule.get_terminals()) for rule in self.rules)
        )

    def get_non_terminals(self):
        return functools.reduce(
            set.union,
            (set(rule.get_non_terminals()) for rule in self.rules)
        )

    def instantiate(self, start: NonTerminal):
        assert start in self.get_non_terminals()
        return Grammar(self, start)


@dataclass
class Grammar:
    schema: GrammarSchema
    start: NonTerminal

    def __post_init__(self):
        assert self.start in self.schema.get_non_terminals(), f'The starting symbol {self.start} must be a non-terminal in {self.schema}'

    def iter_starting_rules(self):
        for rule in self.schema.rules:
            if rule.src == [self.start]:
                yield rule
