from __future__ import annotations

from dataclasses import dataclass, field


class LaTeXNode:
    pass


@dataclass
class Word(LaTeXNode):
    value: str

    def __str__(self):
        return self.value


@dataclass
class Whitespace(LaTeXNode):
    value: str

    def __str__(self):
        return self.value


@dataclass
class Command(LaTeXNode):
    name: str

    def __str__(self):
        return '\\' + self.name


@dataclass
class SpecialNode(LaTeXNode):
    value: str

    def __str__(self):
        return self.value


ampersand = SpecialNode('&')
underscore = SpecialNode('_')
caret = SpecialNode('^')


@dataclass
class Group(LaTeXNode):
    contents: list[LaTeXNode]

    def __str__(self):
        return ''.join(str(node) for node in self.contents)


class BracelessGroup(Group):
    pass


class BraceGroup(Group):
    def __str__(self):
        return '{' + super().__str__() + '}'


class BracketGroup(Group):
    def __str__(self):
        return '[' + super().__str__() + ']'


@dataclass
class Environment(Group):
    name: str

    def __str__(self):
        return '\\begin{%s}' % self.name + super().__str__() + '\\end{%s}' % self.name
