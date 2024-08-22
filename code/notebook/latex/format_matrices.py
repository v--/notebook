from collections.abc import Iterable
from dataclasses import dataclass, field, replace

from ..parsing.parser import Parser
from ..parsing.whitespace import Whitespace
from .nodes import (
    BracketGroup,
    Command,
    Environment,
    Group,
    LaTeXNode,
    SpecialNode,
    stringify_nodes,
)
from .parsing import parse_latex


INDENT = 2


line_break_command = Command('\\')


def strip_whitespace(contents: list[LaTeXNode]) -> list[LaTeXNode]:
    leading = 0
    trailing = 0

    for node in contents:
        if isinstance(node, Whitespace):
            leading += 1
        else:
            break

    for node in reversed(contents):
        if isinstance(node, Whitespace):
            trailing += 1
        else:
            break

    if leading + trailing >= len(contents):
        return []

    if trailing == 0:
        return contents[leading:]

    return contents[leading:-trailing]


@dataclass
class SparseMatrix[T]:
    default: T
    payload: dict[tuple[int, int], T] = field(default_factory=dict)

    def __getitem__(self, index: tuple[int, int]) -> T:
        i, j = index
        return self.payload.get((i, j), self.default)

    def __setitem__(self, index: tuple[int, int], value: T) -> None:
        i, j = index
        self.payload[i, j] = value

    def get_height(self) -> int:
        return max((i + 1 for (i, j) in self.payload), default=0)

    def get_width(self) -> int:
        return max((j + 1 for (i, j) in self.payload), default=0)


@dataclass
class MatrixEnvironment:
    matrix: SparseMatrix[list[LaTeXNode]]
    name: str
    options: BracketGroup | None
    whitespace_prefix_length: int


@dataclass
class MatrixEnvironmentParser(Parser[LaTeXNode]):
    environment_name: str
    whitespace_prefix_length: int

    def skip_whitespace(self) -> None:
        while not self.is_at_end() and isinstance(self.peek(), Whitespace):
            self.advance()

    def advance_and_skip_whitespace(self) -> None:
        self.advance()
        self.skip_whitespace()

    def parse_cell(self) -> list[LaTeXNode]:
        buffer = list[LaTeXNode]()

        while not self.is_at_end() and self.peek() != SpecialNode.ampersand and self.peek() != line_break_command:
            buffer.append(self.peek())
            self.advance()

        return strip_whitespace(buffer)

    def parse_line(self) -> Iterable[list[LaTeXNode]]:
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

    def parse(self) -> MatrixEnvironment:
        env = MatrixEnvironment(
            SparseMatrix(default=[]),
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

    new_matrix: SparseMatrix[list[LaTeXNode]] = SparseMatrix(default=[])

    for j in range(w):
        max_col_width = max(len(stringify_nodes(env.matrix[i, j])) for i in range(h))

        for i in range(h):
            if max_col_width == 0:
                new_matrix[i, j] = []
            elif i == h - 1 and j == w - 1:
                new_matrix[i, j] = env.matrix[i, j]
            else:
                new_matrix[i, j] = env.matrix[i, j] + \
                    [Whitespace.space] * (max_col_width - len(stringify_nodes(env.matrix[i, j])))

    return replace(env, matrix=new_matrix)


def matrix_to_environment(env: MatrixEnvironment) -> Environment:
    contents = list[LaTeXNode]()

    if env.options is not None:
        # Put multi-line options on a new line
        if '\n' in str(env.options):
            contents.append(Whitespace.line_break)
            contents.extend([Whitespace.space] * (env.whitespace_prefix_length + INDENT))

        contents.append(env.options)

    contents.append(Whitespace.line_break)

    w = env.matrix.get_width()
    h = env.matrix.get_height()

    if h == 0:
        contents.extend([Whitespace.space] * env.whitespace_prefix_length)

    for i in range(h):
        for j in range(w):
            if j == 0:
                contents.extend([Whitespace.space] * (env.whitespace_prefix_length + INDENT))

            contents.extend(env.matrix[i, j])

            if j < w - 1:
                if len(stringify_nodes(env.matrix[i, j])) > 0:
                    contents.append(Whitespace.space)

                contents.append(SpecialNode.ampersand)

                if len(stringify_nodes(env.matrix[i, j + 1])) > 0:
                    contents.append(Whitespace.space)
            elif i < h - 1:
                contents.append(Whitespace.space)
                contents.append(line_break_command)
                contents.append(Whitespace.line_break)
            else:
                contents.append(Whitespace.line_break)
                contents.extend([Whitespace.space] * env.whitespace_prefix_length)

    return Environment(name=env.name, contents=contents)


def format_recurse(nodes: Iterable[LaTeXNode], whitespace_prefix_length: int) -> Iterable[LaTeXNode]:
    child_whitespace_prefix_length = whitespace_prefix_length

    for node in nodes:
        match node:
            case Whitespace.line_break:
                child_whitespace_prefix_length = 0
                yield node

            case Whitespace.space:
                child_whitespace_prefix_length += 1
                yield node

            case Whitespace.tab:
                child_whitespace_prefix_length += 4
                yield node

            case Group():
                formatted_contents = list(format_recurse(node.contents, child_whitespace_prefix_length))

                if isinstance(node, Environment):
                    parser = MatrixEnvironmentParser(formatted_contents, node.name, child_whitespace_prefix_length)
                    matrix = parser.parse()
                    aligned_matrix = align_spaces_in_matrix(matrix)
                    yield matrix_to_environment(aligned_matrix)
                else:
                    yield type(node)(contents=formatted_contents)

            case _:
                yield node


def format_tex_matrices(string: str) -> str:
    nodes = parse_latex(string)
    formatted = format_recurse(nodes, whitespace_prefix_length=0)
    return stringify_nodes(formatted)
