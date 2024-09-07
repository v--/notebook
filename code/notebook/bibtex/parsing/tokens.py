from ...parsing.tokens import TokenEnum, TokenMixin
from ...parsing.whitespace import Whitespace


class WordToken(TokenMixin):
    pass


class NumberToken(TokenMixin):
    pass


class SymbolToken(TokenMixin):
    pass


class CommentToken(TokenMixin):
    pass


class MiscToken(TokenEnum):
    at = '@'
    ampersand = '&'
    opening_brace = '{'
    closing_brace = '}'
    backslash = '\\'
    quotes = '"'
    equals = '='
    comma = ','
    underscore = '_'


BibToken = WordToken | NumberToken | SymbolToken | CommentToken | MiscToken | Whitespace
