from ..support.parsing.tokens import TokenMixin, TokenEnum


class LatinLetter(TokenMixin):
    pass


class NaturalNumber(TokenMixin):
    pass


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    l = 'λ'
    dot = '.'
    space = ' '


LambdaToken = LatinLetter | NaturalNumber | MiscToken
