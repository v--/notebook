from ...parsing.tokens import TokenEnum, TokenMixin
from ...parsing.whitespace import Whitespace


class WordToken(TokenMixin):
    pass


class NumberToken(TokenMixin):
    pass


class SymbolToken(TokenMixin):
    pass


class MiscToken(TokenEnum):
    at = '@'
    percent = '%'
    ampersand = '&'
    opening_brace = '{'
    closing_brace = '}'
    backslash = '\\'
    quotes = '"'
    equals = '='
    comma = ','
    underscore = '_'


BibToken = WordToken | NumberToken | SymbolToken | MiscToken | Whitespace
