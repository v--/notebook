from ...support.parsing.tokens import TokenEnum
from ...support.parsing.identifiers import LatinIdentifier, GreekIdentifier
from ...fol.alphabet import PropConstant, BinaryConnective, Quantifier


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
