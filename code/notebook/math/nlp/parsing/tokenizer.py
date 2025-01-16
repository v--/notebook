import unicodedata

from notebook.support.regex import RegexEqual

from ....parsing.tokenizer import Tokenizer
from ....parsing.whitespace import Whitespace
from ..token_sequence import TokenSequence
from ..tokens import NumberToken, SymbolToken, TextToken, WordToken


ALLOWED_INTERWORD_SYMBOLS = frozenset(["'", '`', '-'])


class TextTokenizer(Tokenizer[TextToken]):
    def is_char_letter(self, char: str) -> bool:
        category = unicodedata.category(char)
        return category.startswith('L') or category == 'Mn'

    def is_char_number(self, char: str) -> bool:
        return unicodedata.category(char).startswith('N')

    def parse_word(self) -> WordToken:
        assert self.is_char_letter(self.peek())
        first = self.peek()
        self.advance()
        buffer = first

        while not self.is_at_end():
            head = self.peek()

            if self.is_char_letter(head) or head in ALLOWED_INTERWORD_SYMBOLS:
                buffer += head
                self.advance()
            else:
                break

        return WordToken(buffer)

    def parse_step(self, head: str) -> TextToken:
        if head == Whitespace.space.value:
            self.advance()
            return Whitespace.space

        if head == Whitespace.line_break.value:
            self.advance()
            return Whitespace.line_break

        category = unicodedata.category(head)

        match RegexEqual(category):
            case 'L.' | 'Mn':
                return self.parse_word()

            case 'S.' | 'P.':
                self.advance()
                return SymbolToken(head)

            case 'N.':
                num_string = self.gobble_string(self.is_char_number)
                lookahead = self.peek_multiple(2)

                if len(lookahead) > 0 and lookahead[0] == '-' and self.is_char_letter(lookahead[1]):
                    self.advance()
                    word = self.parse_word()
                    return WordToken(num_string + '-' + str(word))

                return NumberToken(num_string)

            case 'Zs':
                self.advance()
                return Whitespace.space

            case 'Zl' | 'Zp':
                self.advance()
                return Whitespace.line_break

            case _:
                raise self.error(f'Unexpected symbol with category {category}')


def tokenize_text(string: str) -> TokenSequence:
    with TextTokenizer(string) as tokenizer:
        return TokenSequence(tokenizer.parse())
