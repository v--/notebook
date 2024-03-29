from ...support.parsing.tokens import TokenEnum
from ..alphabet import Terminal, NonTerminal


class MiscToken(TokenEnum):
    space = ' '
    epsilon = 'ε'
    right_arrow = '→'
    pipe = '|'
    new_line = '\n'


GrammarToken = Terminal | NonTerminal | MiscToken
