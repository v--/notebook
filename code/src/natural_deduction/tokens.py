from ..support.parsing.tokens import TokenMixin, TokenEnum


class NaturalNumber(TokenMixin):
    pass


class LatinName(TokenMixin):
    pass


class GreekName(TokenMixin):
    pass


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


ContextToken = LatinName | GreekName | NaturalNumber
RuleToken = LatinName | GreekName | NaturalNumber | MiscToken | ContextToken
