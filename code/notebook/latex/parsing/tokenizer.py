from collections.abc import Iterable, Sequence

from ...parsing.tokenizer import Tokenizer
from ...parsing.whitespace import Whitespace
from ...support.iteration import string_accumulator
from ...support.unicode import Capitalization, is_latin_string
from .tokens import EscapedWordToken, LaTeXToken, MiscToken, WordToken


class LaTeXTokenizer(Tokenizer[LaTeXToken]):
    @string_accumulator()
    def read_word(self) -> Iterable[str]:
        while not self.is_at_end() and not (MiscToken.try_match(self.peek()) or Whitespace.try_match(self.peek())):
            yield self.peek()
            self.advance()

    @string_accumulator()
    def read_latin_string(self) -> Iterable[str]:
        while not self.is_at_end() and is_latin_string(self.peek(), capitalization=Capitalization.mixed):
            yield self.peek()
            self.advance()

    def parse_step(self, head: str) -> LaTeXToken:
        token: LaTeXToken | None

        if (token := MiscToken.try_match(head) or Whitespace.try_match(head)):
            self.advance()
            return token

        if head == '\\':
            start = self.index
            self.advance()

            if self.peek() in (' ', '\\', '(', ')', '{', '}'):
                token = EscapedWordToken(self.peek())
                self.advance()
                return token

            if is_latin_string(self.peek(), capitalization=Capitalization.mixed):
                return EscapedWordToken(self.read_latin_string())

            raise self.error('Unrecognized escape character', i_first_token=start)

        return WordToken(self.read_word())


def tokenize_latex(string: str) -> Sequence[LaTeXToken]:
    with LaTeXTokenizer(string) as tokenizer:
        return list(tokenizer.parse())
