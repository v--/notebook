from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.old_tokens import TokenEnum, TokenMixin
from ....parsing.whitespace import Space
from ....support.inference.rules import InferenceRuleConnective
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


LogicTermToken = FunctionSymbolToken | Space | MiscToken | LatinIdentifier
LogicFormulaToken = PredicateSymbolToken | Space | MiscToken | PropConstant | UnaryConnective | BinaryConnective | Quantifier | GreekIdentifier | SchemaConnective

LogicRuleNameToken = SuperscriptToken | CapitalizedLatinString
LogicRuleToken = LogicRuleNameToken | InferenceRuleConnective

LogicToken = LogicTermToken | LogicFormulaToken | LogicRuleToken
