from collections.abc import Iterable, Sequence
from enum import Enum


class StringNode:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, StringNode):
            return type(self) is type(other) and self.value == other.value

        return False


class Text(StringNode):
    pass


class Whitespace(StringNode):
    pass


class Command(StringNode):
    def __str__(self) -> str:
        return '\\' + self.value


class SpecialNode(str, Enum):
    at = '@'
    caret = '^'
    percent = '%'
    ampersand = '&'
    underscore = '_'
    dollar = '$'
    line_break = '\n'

    def __str__(self) -> str:
        return self.value


class Group:
    contents: 'Sequence[LaTeXNode]'

    def __init__(self, contents: 'Sequence[LaTeXNode]') -> None:
        self.contents = contents

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


class Environment(Group):
    name: str

    def __init__(self, name: str, contents: 'Sequence[LaTeXNode]') -> None:
        self.name = name
        super().__init__(contents)

    def __str__(self) -> str:
        return '\\begin{%s}' % self.name + super().__str__() + '\\end{%s}' % self.name


LaTeXNode = Text | Command | SpecialNode | Whitespace | BraceGroup | BracketGroup | Environment


def stringify_nodes(nodes: Iterable[LaTeXNode]) -> str:
    return ''.join(map(str, nodes))
