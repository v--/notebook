from ...support.parsing.tokens import TokenEnum
from ...support.parsing.identifiers import LatinIdentifier, GreekIdentifier

from ..alphabet import PropConstant, BinaryConnective, Quantifier


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    comma = ','
    dot = '.'
    space = ' '

    equality = '='
    negation = '¬'


FOLToken = LatinIdentifier | GreekIdentifier | PropConstant | BinaryConnective | Quantifier | MiscToken
