from collections.abc import Iterable

import bs4
from pydantic import BaseModel

from .....latex.nodes import BraceGroup, Command, LaTeXNode, SpecialNode, Text, Whitespace
from .....latex.parsing import parse_latex
from .....support.iteration import get_strip_slice, string_accumulator
from ...exceptions import BibToolsNotFoundError, BibToolsParsingError


class MathNetEntry(BaseModel):
    RBibitem: str
    by: str
    paper: str
    yr: str
    mathnet: str

    mathscinet: str | None = None
    crossref: str | None = None
    scopus: str | None = None
    zmath: str | None = None
    isi: str | None = None

    vol: str | None = None
    jour: str | None = None
    pages: str | None = None
    publ: str | None = None
    issue: str | None = None
    serial: str | None = None
    publaddr: str | None = None


def iter_amsbib_entry_strings(cursor: bs4.Tag) -> Iterable[str]:
    try:
        head, *tail = cursor.children
    except ValueError:
        return

    yield head.text.lstrip('\n')

    for sub in tail:
        if isinstance(sub, bs4.NavigableString):
            yield sub.text
        elif isinstance(sub, bs4.Tag):
            yield from iter_amsbib_entry_strings(sub)


@string_accumulator('')
def read_amsbib_value(nodes: Iterable[LaTeXNode]) -> Iterable[str]:
    is_in_prefix = True

    for node in nodes:
        match node:
            case Text() | SpecialNode():
                is_in_prefix = False
                yield str(node).replace('~', ' ')

            case BraceGroup():
                is_in_prefix = False
                yield from read_amsbib_value(node.contents)

            case Whitespace():
                if not is_in_prefix:
                    yield str(node)

            case _:
                raise BibToolsParsingError(f'Unexpected LaTeX node of type {type(node).__name__}')


def parse_amsbib_entry_string(string: str) -> tuple[str, str]:
    tokens = parse_latex(string)
    tokens = tokens[get_strip_slice(tokens, lambda token: isinstance(token, Whitespace) or token == SpecialNode.LINE_BREAK)]

    if len(tokens) == 0:
        raise BibToolsParsingError(f'Cannot parse AMSTEX entry line {string!r}')

    command, *rest = tokens

    if isinstance(command, Command):
        return command.value, read_amsbib_value(rest)

    raise BibToolsParsingError(f'Expected a TeX command or newline, got {str(command)!r}')


def parse_mathnet_html(html: str, *, english: bool) -> MathNetEntry:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    container = soup.find(class_='showamsbib')

    if not isinstance(container, bs4.Tag):
        raise BibToolsParsingError('No AMSBIB container element found')

    code_block = container.find(name='code')

    if not isinstance(code_block, bs4.Tag):
        raise BibToolsParsingError('No AMSBIB content found')

    entry_strings = list(iter_amsbib_entry_strings(code_block))
    transl: bool = False
    kv = dict[str, str]()

    for string in entry_strings:
        if len(string) == 0 or string.isspace():
            continue

        key, value = parse_amsbib_entry_string(string)

        match key:
            case 'transl':
                transl = True
                continue

            case 'RBibitem' | 'mathnet' | 'mathscinet' | 'zmath':
                kv[key] = value

            case _ if english == transl:
                kv[key] = value

    if english and not transl:
        raise BibToolsNotFoundError('Could not find English metadata')

    return MathNetEntry.model_validate(kv, strict=True)
