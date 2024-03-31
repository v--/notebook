from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.tokens import TokenEnum
from ...fol.alphabet import BinaryConnective, PropConstant, Quantifier


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    left_bracket = '['
    right_bracket = ']'
    comma = ','
    dot = '.'
    sequent_relation = '⇛'
    colon = ':'
    space = ' '
    negation = '¬'


ContextToken = LatinIdentifier | GreekIdentifier
RuleToken = LatinIdentifier | GreekIdentifier | PropConstant | BinaryConnective | Quantifier | MiscToken | ContextToken
