import unicodedata
from collections.abc import Sequence

from notebook.support.regex import RegexEqual

from ...parsing.tokenizer import Tokenizer
from ...parsing.whitespace import Whitespace
from .tokens import BibToken, MiscToken, NumberToken, SymbolToken, WordToken


class BibTokenizer(Tokenizer[BibToken]):
    def gobble_unicode(self, *codes: str) -> str:
        return self.gobble_string(
            lambda token:
                not MiscToken.try_match(token) and \
                not Whitespace.try_match(token) and \
                any(unicodedata.category(token).startswith(code) for code in codes)
        )

    def parse_step(self, head: str) -> BibToken:
        if (token := MiscToken.try_match(head) or Whitespace.try_match(head)):
            self.advance()
            return token

        category = unicodedata.category(head)

        match RegexEqual(category):
            case 'L.' | 'Mn':
                return WordToken(self.gobble_unicode('L', 'Mn'))

            case 'S.' | 'P.':
                self.advance()
                return SymbolToken(head)

            case 'N.':
                return NumberToken(self.gobble_unicode('N'))

            case _:
                raise self.error(f'Unexpected symbol {head!r} test with category {category}')


def tokenize_bibtex(string: str) -> Sequence[BibToken]:
    with BibTokenizer(string) as tokenizer:
        return list(tokenizer.parse())
