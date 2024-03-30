from ...support.parsing.identifiers import LatinIdentifier
from ...support.parsing.tokens import TokenEnum


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    l = 'λ'
    dot = '.'
    space = ' '


LambdaToken = LatinIdentifier | MiscToken
