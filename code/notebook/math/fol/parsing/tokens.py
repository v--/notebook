from ....parsing.identifiers import GreekIdentifier
from ....parsing.tokens import TokenEnum, TokenMixin
from ....parsing.whitespace import Space
from ..alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective


class FunctionSymbolToken(TokenMixin):
    pass


class PredicateSymbolToken(TokenMixin):
    pass


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    comma = ','
    dot = '.'

    equality = '='
    negation = '¬'


FOLToken = FunctionSymbolToken | PredicateSymbolToken | GreekIdentifier | PropConstant | BinaryConnective | Quantifier | UnaryConnective | MiscToken | Space
