from ...support.parsing.identifiers import GreekIdentifier, LatinIdentifier
from ...support.parsing.tokens import TokenEnum
from ..alphabet import BinaryConnective, PropConstant, Quantifier


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    comma = ','
    dot = '.'
    space = ' '

    equality = '='
    negation = '¬'


FOLToken = LatinIdentifier | GreekIdentifier | PropConstant | BinaryConnective | Quantifier | MiscToken
