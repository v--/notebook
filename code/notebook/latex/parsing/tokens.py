from ...parsing.tokens import TokenEnum, TokenMixin
from ...parsing.whitespace import Whitespace


class WordToken(TokenMixin):
    pass


class EscapedWordToken(TokenMixin):
    def __str__(self) -> str:
        return '\\' + self.value


class MiscToken(TokenEnum):
    ampersand = '&'
    underscore = '_'
    caret = '^'
    opening_brace = '{'
    closing_brace = '}'
    opening_bracket = '['
    closing_bracket = ']'


LaTeXToken = WordToken | EscapedWordToken | Whitespace | MiscToken
