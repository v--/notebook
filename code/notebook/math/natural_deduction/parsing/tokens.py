
from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.tokens import TokenEnum, TokenMixin
from ....parsing.whitespace import Space
from ...fol.alphabet import BinaryConnective, PropConstant, Quantifier, UnaryConnective


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    left_bracket = '['
    right_bracket = ']'
    comma = ','
    dot = '.'
    sequent_relation = '⫢'
    colon = ':'


class SuperscriptToken(TokenEnum):
    plus = '⁺'
    minus = '⁻'
    left = 'ᴸ'
    right = 'ᴿ'


class CapitalLatinString(TokenMixin):
    pass


RuleToken = LatinIdentifier | GreekIdentifier | PropConstant | BinaryConnective | Quantifier | UnaryConnective | MiscToken | SuperscriptToken | CapitalLatinString | Space
