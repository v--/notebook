from ....parsing.tokens import TokenMixin
from ....parsing.whitespace import Whitespace


class WordToken(TokenMixin):
    pass


class NumberToken(TokenMixin):
    pass


class SymbolToken(TokenMixin):
    pass


TextToken = WordToken | NumberToken | SymbolToken | Whitespace
