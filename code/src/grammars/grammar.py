from __future__ import annotations

from dataclasses import dataclass, field
import itertools
import functools
from typing import cast

from ..support.tokenization import Tokenizer


@dataclass
@functools.total_ordering
class GrammarSymbol:
    value: str

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: object):
        return type(self) == type(other) and self.value == cast(GrammarSymbol, other).value

    def __le__(self, other: object):
        return type(self) == type(other) and self.value <= cast(GrammarSymbol, other).value


@dataclass
@functools.total_ordering
class Epsilon:
    def __str__(self):
        return f'ε'

    def __hash__(self):
        return hash('ε')

    def __eq__(self, other: object):
        return type(self) == type(other)

    def __le__(self, other: object):
        return type(self) == type(other)


@dataclass
@functools.total_ordering
class RightArrow:
    def __str__(self):
        return f'→'

    def __hash__(self):
        return hash('→')

    def __eq__(self, other: object):
        return type(self) == type(other)

    def __le__(self, other: object):
        return type(self) == type(other)


class Terminal(GrammarSymbol):
    def __str__(self):
        return f'"{self.value}"'


class NonTerminal(GrammarSymbol):
    def __str__(self):
        return f'<{self.value}>'


@dataclass
class GrammarRuleTokenizer(Tokenizer):
    def parse_string(self, delim_a: str, delim_b: str):
        assert self.peek() == delim_a
        self.advance()
        buffer = ''

        while self.peek() != delim_b:
            assert not self.is_at_end(), f'String not closed: {delim_a}{buffer}'
            assert self.peek() != delim_a, f'Strings are not recursive: {delim_a} cannot occur after {delim_a}{buffer}'

            if self.peek(2) in (r'\<', r'\>', r'\"', r'\\'):
                self.advance()
                buffer += self.peek()
                self.advance()
            else:
                buffer += self.peek()
                self.advance()

        self.advance()
        return buffer

    def tokenize(self):
        while not self.is_at_end():
            if self.peek() == 'ε':
                yield Epsilon()
                self.advance()

            elif self.peek() == '→':
                yield RightArrow()
                self.advance()

            elif self.peek() == '<':
                yield NonTerminal(self.parse_string('<', '>'))

            elif self.peek() == '"':
                yield Terminal(self.parse_string('"', '"'))

            elif self.peek() == ' ':
                self.advance()

            else:
                assert False, f'unexpected symbol {self.peek()}'


@dataclass
class GrammarRule:
    src: list[Terminal | NonTerminal]
    dest: list[Terminal | NonTerminal | Epsilon]

    def __post_init__(self):
        assert any(isinstance(sym, NonTerminal) for sym in self.src), 'The source must contain at least one non-terminal, but it is {}'.format(' '.join(str(sym) for sym in self.src))

    @classmethod
    def parse(cls, string: str):
        src: list[Terminal | NonTerminal] = []
        dest: list[Terminal | NonTerminal | Epsilon] = []
        in_dest = False

        for token in GrammarRuleTokenizer(string).tokenize():
            if isinstance(token, Terminal) or isinstance(token, NonTerminal):
                if in_dest:
                    assert Epsilon() not in dest, f'Syntax error: unexpected {token} in rule {string}'
                    dest.append(token)
                else:
                    src.append(token)
            elif isinstance(token, RightArrow) and any(isinstance(t, NonTerminal) for t in src) and len(dest) == 0:
                in_dest = True
            elif isinstance(token, Epsilon) and in_dest and len(dest) == 0:
                dest.append(token)
            else:
                assert not isinstance(token, RightArrow), f'Syntax error: unexpected → in rule {string}'
                assert not isinstance(token, Epsilon), f'Syntax error: unexpected ε in rule {string}'

        return cls(src, dest)

    @property
    def is_epsilon(self):
        return self.dest == [Epsilon()]

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
    rules: set[GrammarRule] = field(default_factory=set)

    def __str__(self):
        return '\n'.join(str(rule) for rule in self.rules)

    def add_rule(self, string: str):
        self.rules.add(GrammarRule.parse(string))

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

    def instantiate_grammar(self, start: str):
        return Grammar(self, NonTerminal(start))


@dataclass
class Grammar:
    schema: GrammarSchema
    start: NonTerminal

    def __post_init__(self):
        assert self.start in self.schema.get_non_terminals(), f'The starting symbol {self.start} must be a non-terminal in {self.schema}'
