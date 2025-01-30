from ....parsing.identifiers import GreekIdentifier, LatinIdentifier
from ....parsing.tokens import TokenEnum, TokenMixin
from ....parsing.whitespace import Space
from ....support.inference.rules import InferenceRuleConnective
from ..alphabet import BinaryTypeConnective, TermConnective, TypeAssertionConnective


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


TermToken = ConstantTermToken | LatinIdentifier | MiscToken | TermConnective
SimpleTypeToken = BaseTypeToken | GreekIdentifier | MiscToken | Space | BinaryTypeConnective
TypeAssertionToken = Space | TypeAssertionConnective
TypingRuleToken = MiscToken | Space | InferenceRuleConnective
LambdaToken = TermToken | SimpleTypeToken | TypeAssertionToken | TypingRuleToken
