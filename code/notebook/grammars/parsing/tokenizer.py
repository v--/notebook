from ...support.parsing.tokenizer import Tokenizer
from ...support.parsing.whitespace import Whitespace
from ..alphabet import NonTerminal, Terminal
from .tokens import GrammarToken, MiscToken


class GrammarTokenizer(Tokenizer[GrammarToken]):
    def parse_non_terminal(self) -> NonTerminal:
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
        return NonTerminal(''.join(buffer))

    def parse_terminal(self) -> Terminal:
        assert self.peek() == '"'
        self.advance()
        value = self.peek()

        if value == '"':
            raise self.error('Empty terminals are disallowed')

        self.advance()

        if self.peek() != '"':
            raise self.error('Multi-symbol terminals are disallowed')

        self.advance()
        return Terminal(value)

    def parse_step(self, head: str) -> GrammarToken:
        sym = MiscToken.try_match(head) or Whitespace.try_match(head)

        if sym is not None:
            self.advance()
            return sym

        if head == '<':
            return self.parse_non_terminal()

        if head == '"':
            return self.parse_terminal()

        raise self.error('Unexpected symbol')
