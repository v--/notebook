from ...parsing.tokens import TokenEnum, TokenMixin


class WordToken(TokenMixin):
    pass


class EscapedWordToken(TokenMixin):
    def __str__(self):
        return '\\' + self.value


class WhitespaceToken(TokenMixin):
    pass


class SpecialToken(TokenEnum):
    ampersand_token = '&'
    underscore_token = '_'
    caret_token = '^'
    opening_brace = '{'
    closing_brace = '}'
    opening_bracket = '['
    closing_bracket = ']'


LaTeXToken = WordToken | EscapedWordToken | WhitespaceToken | SpecialToken
