from collections.abc import Iterable, Sequence
from dataclasses import dataclass

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


@dataclass(frozen=True)
class Group:
    contents: 'Sequence[LaTeXNode]'

    def __str__(self) -> str:
        return ''.join(str(node) for node in self.contents)

    def __hash__(self) -> int:
        return hash(tuple(self.contents))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Group):
            return all(a == b for a, b in zip(self.contents, other.contents, strict=True))

        return False


class BraceGroup(Group):
    def __str__(self) -> str:
        return '{' + super().__str__() + '}'


class BracketGroup(Group):
    def __str__(self) -> str:
        return '[' + super().__str__() + ']'


@dataclass(frozen=True)
class Environment(Group):
    name: str

    def __str__(self) -> str:
        return '\\begin{%s}' % self.name + super().__str__() + '\\end{%s}' % self.name


LaTeXNode = Word | Command | SpecialNode | Whitespace | BraceGroup | BracketGroup | Environment


def stringify_nodes(nodes: Iterable[LaTeXNode]) -> str:
    return ''.join(map(str, nodes))
