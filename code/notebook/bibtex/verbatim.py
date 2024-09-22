from ..latex.nodes import BraceGroup
from ..latex.parsing import parse_latex
from ..parsing.parser import ParsingError


def is_verbatim_string(string: str) -> bool:
    try:
        nodes = parse_latex(string)
    except ParsingError:
        return False

    return len(nodes) == 1 and isinstance(nodes[0], BraceGroup)


def strip_outer_braces(string: str) -> str:
    try:
        nodes = parse_latex(string)
    except ParsingError:
        return string

    if len(nodes) == 1 and isinstance(nodes[0], BraceGroup):
        return ''.join(map(str, nodes[0].contents))

    return string
