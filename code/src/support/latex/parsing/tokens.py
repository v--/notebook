from ...parsing.tokens import TokenEnum, TokenMixin


class WordToken(TokenMixin):
    pass


class EscapedWordToken(TokenMixin):
    def __str__(self):
        return '\\' + self.value


class MiscToken(TokenEnum):
    line_break = '\n'
    tab = '\t'
    space = ' '
    ampersand = '&'
    underscore = '_'
    caret = '^'
    opening_brace = '{'
    closing_brace = '}'
    opening_bracket = '['
    closing_bracket = ']'


LaTeXToken = WordToken | EscapedWordToken | MiscToken
