from collections.abc import Sequence
from dataclasses import dataclass, field
import functools
import itertools
from typing import Literal

from ..support.parsing import Parser, TokenEnum, TokenMixin


class Terminal(TokenMixin):
    def __str__(self):
        return f'"{self.value}"'


class NonTerminal(TokenMixin):
    def __str__(self):
        return f'<{self.value}>'


class SingletonSymbol(TokenEnum):
    epsilon = 'ε'
    right_arrow = '→'
    pipe = '|'
    new_line = '\n'


GrammarSymbol = Terminal | NonTerminal | Literal[SingletonSymbol.epsilon]


class GrammarTokenizer(Parser[str]):
    def parse_non_terminal(self):
        assert self.peek() == '<'
        self.advance()
        buffer: list[str] = []

        while self.peek() != '>':
            if self.is_at_end():
                raise self.error('Nonterminal identifier not closed', precede=len(buffer) + 1)

            if self.peek() == '<':
                raise self.error('Nonterminal names cannot be nested', precede=len(buffer) + 1)

            if self.peek() == '\\':
                self.advance()

                if self.peek() in ('<', '>', '\\'):
                    buffer.append(self.peek())
                else:
                    raise self.error('Invalid escape code', precede=1)

                self.advance()
            else:
                buffer.append(self.peek())
                self.advance()

        self.advance()
        return ''.join(buffer)

    def parse(self):
        while not self.is_at_end():
            sym = self.parse_step(self.peek())

            if sym is not None:
                yield sym

    def parse_step(self, head: str):
        match head:
            case '<':
                return NonTerminal(self.parse_non_terminal())

            case '"':
                self.advance()
                value = self.peek()

                if value == '"':
                    raise self.error('Empty terminals are disallowed')

                self.advance()

                if self.peek() != '"':
                    raise self.error('Multi-symbol terminals are disallowed')

                self.advance()
                return Terminal(value)

            case ' ':
                self.advance()

            case _ if SingletonSymbol.try_match(head):
                self.advance()
                return SingletonSymbol(head)

            case _:
                raise self.error('Unexpected symbol')


class GrammarParser(Parser[Sequence[Terminal | NonTerminal | SingletonSymbol]]):
    def parse(self):
        src: list[Terminal | NonTerminal] = []
        dest: list[GrammarSymbol] = []
        in_dest = False

        while not self.is_at_end():
            symbol = self.peek()

            match symbol:
                case SingletonSymbol.new_line | SingletonSymbol.pipe:
                    if in_dest and len(dest) > 0:
                        yield src, dest
                    elif len(src) > 0:
                        raise self.error('Attempting to end an incomplete rule')

                    if symbol == SingletonSymbol.new_line:
                        src = []
                        in_dest = False

                    dest = []
                    self.advance()

                case Terminal() | NonTerminal():
                    if in_dest:
                        if SingletonSymbol.epsilon in dest:
                            raise self.error(f'Unexpected {symbol} after ε')

                        dest.append(symbol)
                    else:
                        src.append(symbol)

                    self.advance()

                case SingletonSymbol.epsilon:
                    if in_dest and len(dest) == 0:
                        dest.append(SingletonSymbol.epsilon)
                    else:
                        raise self.error('ε is only allowed on its own on the right side of a rule')

                    self.advance()

                case SingletonSymbol.right_arrow:
                    if in_dest:
                        raise self.error('Only one → allowed per line')

                    in_dest = True
                    self.advance()

                case _:
                    self.advance()


@dataclass
class GrammarRule:
    src: list[Terminal | NonTerminal]
    dest: list[GrammarSymbol]

    def __post_init__(self):
        assert any(isinstance(sym, NonTerminal) for sym in self.src), 'The source must contain at least one nonterminal, but it is {}'.format(' '.join(str(sym) for sym in self.src))
        assert all(sym != SingletonSymbol.epsilon for sym in self.dest) or len(self.dest) == 1, 'SingletonSymbol.epsilon rules cannot contain other symbols, got {}'.format(' '.join(str(sym) for sym in self.dest))
        assert all(len(sym.value) == 1 for sym in itertools.chain(self.src, self.dest) if isinstance(sym, Terminal)), 'Multi-symbol terminals are disallowed'

    @classmethod
    def parse(cls, string: str):
        tokens = list(GrammarTokenizer(string).parse())

        for src, dest in GrammarParser(tokens).parse():
            yield cls(src, dest)

    @property
    def src_symbol(self) -> NonTerminal:
        assert len(self.src) == 1
        assert isinstance(self.src[0], NonTerminal)
        return self.src[0]

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
        assert self.start in self.schema.get_non_terminals(), f'The starting symbol {self.start} must be a nonterminal in {self.schema}'

    def iter_starting_rules(self):
        for rule in self.schema.rules:
            if rule.src == [self.start]:
                yield rule
