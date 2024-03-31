from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ..alphabet import NonTerminal, Terminal
from .tokens import GrammarToken, MiscToken


class GrammarTokenizer(Tokenizer[GrammarToken]):
    def parse_non_terminal(self) -> NonTerminal:
        assert self.peek() == '<'
        start = self.index
        self.advance()
        buffer: list[str] = []

        while self.peek() != '>':
            if self.peek() == '<':
                raise self.error('Nonterminal names cannot be nested', i_first_token=start)

            if self.peek() == '\\':
                self.advance()

                if self.peek() in ('<', '>', '\\'):
                    buffer.append(self.peek())
                else:
                    raise self.error('Invalid escape code', i_first_token=self.index - 1)

                self.advance()
            else:
                buffer.append(self.peek())
                self.advance()

            if self.is_at_end():
                raise self.error('Nonterminal has no matching end bracket', i_first_token=start)


        if len(buffer) == 0:
            raise self.error('Empty nonterminals are disallowed', i_first_token=start)

        self.advance()
        return NonTerminal(''.join(buffer))

    def parse_terminal(self) -> Terminal:
        assert self.peek() == '"'
        start = self.index
        self.advance()
        value = self.peek()

        if value == '"':
            raise self.error('Empty terminals are disallowed', i_first_token=start)

        self.advance()

        if self.is_at_end():
            raise self.error('Terminal has no matching end quote', i_first_token=start)

        if not self.is_at_end() and self.peek() != '"':
            raise self.error('Multi-symbol terminals are disallowed', i_first_token=start)

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


def tokenize_bnf(string: str) -> list[GrammarToken]:
    tokenizer = GrammarTokenizer(string)
    tokens = list(tokenizer.parse())
    tokenizer.assert_exhausted()
    return tokens
