from ...support.parsing.tokens import TokenEnum
from ...support.parsing.whitespace import Whitespace
from ..alphabet import NonTerminal, Terminal


class MiscToken(TokenEnum):
    epsilon = 'ε'
    right_arrow = '→'
    pipe = '|'


GrammarToken = Terminal | NonTerminal | Whitespace | MiscToken
