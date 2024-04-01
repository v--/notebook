from ....parsing.identifiers import LatinIdentifier
from ....parsing.tokens import TokenEnum
from ....parsing.whitespace import Space


class MiscToken(TokenEnum):
    left_parenthesis = '('
    right_parenthesis = ')'
    l = 'λ'
    dot = '.'


LambdaToken = LatinIdentifier | Space | MiscToken
