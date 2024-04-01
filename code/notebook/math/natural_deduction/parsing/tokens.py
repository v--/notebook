from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.tokens import TokenEnum
from ....parsing.whitespace import Space
from ...fol.alphabet import BinaryConnective, PropConstant, Quantifier


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    left_bracket = '['
    right_bracket = ']'
    comma = ','
    dot = '.'
    sequent_relation = '⫢'
    colon = ':'
    negation = '¬'


ContextToken = LatinIdentifier | GreekIdentifier | Space
RuleToken = LatinIdentifier | GreekIdentifier | PropConstant | BinaryConnective | Quantifier | MiscToken | ContextToken | Space
