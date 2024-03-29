from ..support.parsing.tokens import TokenEnum
from ..support.parsing.identifiers import LatinIdentifier


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    l = 'λ'
    dot = '.'
    space = ' '


LambdaToken = LatinIdentifier | MiscToken
