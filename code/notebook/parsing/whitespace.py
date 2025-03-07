from typing import Literal

from .old_tokens import TokenEnum


class Whitespace(TokenEnum):
    line_break = '\n'
    tab = '\t'
    space = ' '


Space = Literal[Whitespace.space]
Tab = Literal[Whitespace.tab]
LineBreak = Literal[Whitespace.line_break]
