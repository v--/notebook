import functools
import operator
from dataclasses import dataclass
from typing import Iterable

from ..parsing.tokens import TokenEnum, TokenMixin
from ..parsing.whitespace import Whitespace


class Word(TokenMixin):
    pass


class Command(TokenMixin):
    def __str__(self) -> str:
        return '\\' + self.value


class SpecialNode(TokenEnum):
    ampersand = '&'
    underscore = '_'
    caret = '^'


@dataclass
class Group:
    contents: 'list[LaTeXNode]'

    def __str__(self) -> str:
        return ''.join(str(node) for node in self.contents)

    def __hash__(self) -> int:
        return functools.reduce(operator.xor, map(hash, self.contents), 0)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Group):
            return all(a == b for a, b in zip(self.contents, other.contents))

        return False


class BraceGroup(Group):
    def __str__(self) -> str:
        return '{' + super().__str__() + '}'


class BracketGroup(Group):
    def __str__(self) -> str:
        return '[' + super().__str__() + ']'


@dataclass
class Environment(Group):
    name: str

    def __str__(self) -> str:
        return '\\begin{%s}' % self.name + super().__str__() + '\\end{%s}' % self.name  # noqa: UP031


LaTeXNode = Word | Command | SpecialNode | Whitespace | BraceGroup | BracketGroup | Environment


def stringify_nodes(nodes: Iterable[LaTeXNode]) -> str:
    return ''.join(map(str, nodes))
