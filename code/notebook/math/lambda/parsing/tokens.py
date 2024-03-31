from ....parsing.identifiers import LatinIdentifier
from ....parsing.tokens import TokenEnum


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    l = 'λ'
    dot = '.'
    space = ' '


LambdaToken = LatinIdentifier | MiscToken
