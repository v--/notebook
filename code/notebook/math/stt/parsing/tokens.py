from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.tokens import TokenEnum, TokenMixin
from ....parsing.whitespace import Space
from ..alphabet import LambdaTermConnective, RuleConnective, SimpleTypeConnective, TypeAssertionConnective


class CapitalizedLatinString(TokenMixin):
    pass


class ConstantTermToken(TokenMixin):
    pass


class BaseTypeToken(TokenMixin):
    pass


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    left_bracket = '['
    right_bracket = ']'
    dot = '.'
    comma = ','


LambdaTermToken = ConstantTermToken | LatinIdentifier | MiscToken | LambdaTermConnective
SimpleTypeToken = BaseTypeToken | GreekIdentifier | MiscToken | Space | SimpleTypeConnective
TypeAssertionToken = Space | TypeAssertionConnective
TypeRuleToken = MiscToken | Space | RuleConnective
STTToken = LambdaTermToken | SimpleTypeToken | TypeAssertionToken | TypeRuleToken
