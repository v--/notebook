from dataclasses import dataclass, field, replace
from typing import Generic, Iterator, TypeVar

from ..parsing.parser import Parser
from ..parsing.whitespace import Whitespace
from .nodes import (
    BracelessGroup,
    BracketGroup,
    Command,
    Environment,
    Group,
    LaTeXNode,
    SpecialNode,
)
from .parsing.parser import parse_latex


INDENT = 2


line_break_command = Command('\\')
empty_group = BracelessGroup(contents=[])


def strip_whitespace(grp: BracelessGroup):
    leading = 0
    trailing = 0

    for node in grp.contents:
        if isinstance(node, Whitespace):
            leading += 1
        else:
            break

    for node in reversed(grp.contents):
        if isinstance(node, Whitespace):
            trailing += 1
        else:
            break

    if leading + trailing >= len(grp.contents):
        return BracelessGroup([])

    if trailing == 0:
        return BracelessGroup(grp.contents[leading:])

    return BracelessGroup(grp.contents[leading:-trailing])


T = TypeVar('T')


@dataclass
class SparseMatrix(Generic[T]):
    default: T
    payload: dict[tuple[int, int], T] = field(default_factory=dict)

    def __getitem__(self, index: tuple[int, int]):
        i, j = index
        return self.payload.get((i, j), self.default)

    def __setitem__(self, index: tuple[int, int], value: T):
        i, j = index
        self.payload[i, j] = value

    def get_height(self):
        return max((i + 1 for (i, j) in self.payload.keys()), default=0)

    def get_width(self):
        return max((j + 1 for (i, j) in self.payload.keys()), default=0)


@dataclass
class MatrixEnvironment:
    matrix: SparseMatrix[LaTeXNode]
    name: str
    options: BracketGroup | None
    whitespace_prefix_length: int


@dataclass
class MatrixEnvironmentParser(Parser[LaTeXNode]):
    environment_name: str
    whitespace_prefix_length: int

    def skip_whitespace(self):
        while not self.is_at_end() and isinstance(self.peek(), Whitespace):
            self.advance()

    def advance_and_skip_whitespace(self):
        self.advance()
        self.skip_whitespace()

    def parse_cell(self) -> BracelessGroup:
        buffer: list[LaTeXNode] = []

        while not self.is_at_end() and self.peek() != SpecialNode.ampersand and self.peek() != line_break_command:
            buffer.append(self.peek())
            self.advance()

        return strip_whitespace(BracelessGroup(buffer))

    def parse_line(self) -> Iterator[BracelessGroup]:
        while not self.is_at_end():
            yield self.parse_cell()

            if self.is_at_end():
                return

            if self.peek() == line_break_command:
                self.advance_and_skip_whitespace()
                return

            if self.peek() == SpecialNode.ampersand:
                self.advance_and_skip_whitespace()
            else:
                raise self.error('Unexpected node')

    def parse(self):
        env = MatrixEnvironment(
            SparseMatrix(default=empty_group),
            self.environment_name, None,
            self.whitespace_prefix_length
        )

        self.skip_whitespace()

        if not self.is_at_end() and isinstance(head := self.peek(), BracketGroup):
            env.options = head
            self.advance_and_skip_whitespace()

        i = 0

        while not self.is_at_end():
            for j, cell in enumerate(self.parse_line()):
                env.matrix[i, j] = cell

            i += 1

        return env


def align_spaces_in_matrix(env: MatrixEnvironment) -> MatrixEnvironment:
    w = env.matrix.get_width()
    h = env.matrix.get_height()

    new_matrix: SparseMatrix[LaTeXNode] = SparseMatrix(default=empty_group)

    for j in range(w):
        max_col_width = max(len(str(env.matrix[i, j])) for i in range(h))

        for i in range(h):
            # print(repr(env.matrix[i, j]))
            if max_col_width == 0:
                new_matrix[i, j] = BracelessGroup([])
            elif i == h - 1 and j == w - 1:
                new_matrix[i, j] = BracelessGroup([env.matrix[i, j]])
            else:
                new_matrix[i, j] = BracelessGroup(
                    [env.matrix[i, j]] + \
                    [Whitespace.space] * (max_col_width - len(str(env.matrix[i, j])))
                )

    return replace(env, matrix=new_matrix)


def matrix_to_environment(env: MatrixEnvironment):
    result = Environment(name=env.name, contents=[])

    if env.options is not None:
        # Put multiline options on a new line
        if '\n' in str(env.options):
            result.contents.append(Whitespace.line_break)
            result.contents.extend([Whitespace.space] * (env.whitespace_prefix_length + INDENT))

        result.contents.append(env.options)

    result.contents.append(Whitespace.line_break)

    w = env.matrix.get_width()
    h = env.matrix.get_height()

    if h == 0:
        result.contents.extend([Whitespace.space] * env.whitespace_prefix_length)

    for i in range(h):
        for j in range(w):
            if j == 0:
                result.contents.extend([Whitespace.space] * (env.whitespace_prefix_length + INDENT))

            result.contents.append(env.matrix[i, j])

            if j < w - 1:
                if len(str(env.matrix[i, j])) > 0:
                    result.contents.append(Whitespace.space)

                result.contents.append(SpecialNode.ampersand)

                if len(str(env.matrix[i, j + 1])) > 0:
                    result.contents.append(Whitespace.space)
            elif i < h - 1:
                result.contents.append(Whitespace.space)
                result.contents.append(line_break_command)
                result.contents.append(Whitespace.line_break)
            else:
                result.contents.append(Whitespace.line_break)
                result.contents.extend([Whitespace.space] * env.whitespace_prefix_length)

    return result


def format_recurse(node: LaTeXNode, whitespace_prefix_length: int):
    if not isinstance(node, Group):
        return node

    new_contents: list[LaTeXNode] = []
    child_whitespace_prefix_length = whitespace_prefix_length

    for child in node.contents:
        match child:
            case Whitespace.line_break:
                child_whitespace_prefix_length = 0
                new_contents.append(child)

            case Whitespace.space:
                child_whitespace_prefix_length += 1
                new_contents.append(child)

            case Whitespace.tab:
                child_whitespace_prefix_length += 4
                new_contents.append(child)

            case _:
                new_child = format_recurse(child, child_whitespace_prefix_length)
                new_contents.append(new_child)

    if isinstance(node, Environment):
        parser = MatrixEnvironmentParser(new_contents, node.name, whitespace_prefix_length)
        matrix = parser.parse()
        aligned_matrix = align_spaces_in_matrix(matrix)
        return matrix_to_environment(aligned_matrix)

    return type(node)(contents=new_contents)


def format_tex_matrices(string: str):
    parsed = parse_latex(string)
    new = format_recurse(parsed, whitespace_prefix_length=0)
    return str(new)
