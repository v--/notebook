from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.tokens import TokenEnum, TokenMixin
from ....parsing.whitespace import Space
from ...stt.alphabet import RuleConnective
from ..alphabet import BinaryConnective, PropConstant, Quantifier, SchemaConnective, UnaryConnective


class CapitalizedLatinString(TokenMixin):
    pass


class FunctionSymbolToken(TokenMixin):
    pass


class PredicateSymbolToken(TokenMixin):
    pass


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    left_bracket = '['
    right_bracket = ']'
    comma = ','
    dot = '.'
    star = '*'
    equality = '='


class SuperscriptToken(TokenEnum):
    plus = '⁺'
    minus = '⁻'
    left = 'ᴸ'
    right = 'ᴿ'


FOLTermToken = FunctionSymbolToken | Space | MiscToken | LatinIdentifier
FOLFormulaToken = PredicateSymbolToken | Space | MiscToken | PropConstant | UnaryConnective | BinaryConnective | Quantifier | GreekIdentifier | SchemaConnective

FOLRuleNameToken = SuperscriptToken | CapitalizedLatinString
FOLRuleToken = FOLRuleNameToken | RuleConnective

FOLToken = FOLTermToken | FOLFormulaToken | FOLRuleToken
