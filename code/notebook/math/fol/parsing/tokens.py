from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.tokens import TokenEnum
from ....parsing.whitespace import Space
from ..alphabet import BinaryConnective, PropConstant, Quantifier


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    comma = ','
    dot = '.'

    equality = '='
    negation = '¬'


FOLToken = LatinIdentifier | GreekIdentifier | PropConstant | BinaryConnective | Quantifier | MiscToken | Space
