from collections.abc import Iterable, MutableMapping, Sequence
from dataclasses import dataclass, field

from ..support.iteration import get_strip_slice
from .nodes import (
    BracketGroup,
    Command,
    Environment,
    Group,
    LaTeXNode,
    SpecialNode,
    Whitespace,
    stringify_nodes,
)
from .parsing import parse_latex


INDENT = 2
LINE_BREAK_COMMAND = Command('\\')


@dataclass
class SparseMatrix[T]:
    default: T
    _payload: MutableMapping[tuple[int, int], T] = field(default_factory=dict)

    def __getitem__(self, index: tuple[int, int]) -> T:
        i, j = index
        return self._payload.get((i, j), self.default)

    def __setitem__(self, index: tuple[int, int], value: T) -> None:
        i, j = index
        self._payload[i, j] = value

    def get_height(self) -> int:
        return max((i + 1 for (i, j) in self._payload), default=0)

    def get_width(self) -> int:
        return max((j + 1 for (i, j) in self._payload), default=0)


@dataclass
class MatrixEnvironment:
    matrix: SparseMatrix[Sequence[LaTeXNode]]
    name: str
    options: BracketGroup | None
    whitespace_prefix_length: int


class MatrixEnvironmentParser:
    tokens: Sequence[LaTeXNode]
    token_index: int
    environment_name: str
    whitespace_prefix_length: int

    def __init__(self, tokens: Sequence[LaTeXNode], environment_name: str, whitespace_prefix_length: int) -> None:
        self.tokens = tokens
        self.environment_name = environment_name
        self.whitespace_prefix_length = whitespace_prefix_length
        self.token_index = 0

    def peek(self) -> LaTeXNode | None:
        try:
            return self.tokens[self.token_index]
        except IndexError:
            return None

    def advance(self, count: int = 1) -> None:
        self.token_index += count

    def skip_whitespace_and_line_breaks(self) -> None:
        while (head := self.peek()) and (head == SpecialNode.LINE_BREAK or isinstance(head, Whitespace)):
            self.advance()

    def _parse_cell(self) -> Sequence[LaTeXNode]:
        buffer = list[LaTeXNode]()

        while (head := self.peek()) and head != SpecialNode.AMPERSAND and head != LINE_BREAK_COMMAND:
            buffer.append(head)
            self.advance()

        # return strip_whitespace_and_line_breaks(buffer)
        return buffer[get_strip_slice(buffer, lambda token: isinstance(token, Whitespace) or token == SpecialNode.LINE_BREAK)]

    def _parse_line(self) -> Iterable[Sequence[LaTeXNode]]:
        while self.peek():
            yield self._parse_cell()

            head = self.peek()

            if not head:
                return

            if head == LINE_BREAK_COMMAND:
                self.advance()
                self.skip_whitespace_and_line_breaks()
                return

            self.advance()
            self.skip_whitespace_and_line_breaks()

    def parse(self) -> MatrixEnvironment:
        env = MatrixEnvironment(
            SparseMatrix(default=[]),
            self.environment_name, None,
            self.whitespace_prefix_length
        )

        self.skip_whitespace_and_line_breaks()

        if (head := self.peek()) and isinstance(head, BracketGroup):
            env.options = head

            self.advance()
            self.skip_whitespace_and_line_breaks()

        i = 0

        while self.peek():
            for j, cell in enumerate(self._parse_line()):
                env.matrix[i, j] = cell

            i += 1

        return env


def align_spaces_in_matrix(env: MatrixEnvironment) -> MatrixEnvironment:
    w = env.matrix.get_width()
    h = env.matrix.get_height()

    new_matrix: SparseMatrix[Sequence[LaTeXNode]] = SparseMatrix(default=[])

    for j in range(w):
        max_col_width = max(len(stringify_nodes(env.matrix[i, j])) for i in range(h))

        for i in range(h):
            if max_col_width == 0:
                new_matrix[i, j] = []
            elif i == h - 1 and j == w - 1:
                new_matrix[i, j] = env.matrix[i, j]
            else:
                new_cell = list(env.matrix[i, j])
                new_cell.append(
                    Whitespace(' ' * (max_col_width - len(stringify_nodes(env.matrix[i, j]))))
                )

                new_matrix[i, j] = new_cell

    return MatrixEnvironment(
        name=env.name,
        options=env.options,
        whitespace_prefix_length=env.whitespace_prefix_length,
        matrix=new_matrix
    )


def matrix_to_environment(env: MatrixEnvironment) -> Environment:
    contents = list[LaTeXNode]()

    if env.options is not None:
        # Put multi-line options on a new line
        if '\n' in str(env.options):
            contents.append(SpecialNode.LINE_BREAK)
            contents.append(Whitespace(' ' * (env.whitespace_prefix_length + INDENT)))

        contents.append(env.options)

    contents.append(SpecialNode.LINE_BREAK)

    w = env.matrix.get_width()
    h = env.matrix.get_height()

    if h == 0:
        contents.append(
            Whitespace(' ' * env.whitespace_prefix_length)
        )

    for i in range(h):
        for j in range(w):
            if j == 0:
                contents.append(
                    Whitespace(' ' * (env.whitespace_prefix_length + INDENT))
                )

            contents.extend(env.matrix[i, j])

            if j < w - 1:
                if len(stringify_nodes(env.matrix[i, j])) > 0:
                    contents.append(Whitespace(' '))

                contents.append(SpecialNode.AMPERSAND)

                if len(stringify_nodes(env.matrix[i, j + 1])) > 0:
                    contents.append(Whitespace(' '))
            elif i < h - 1:
                contents.append(Whitespace(' '))
                contents.append(LINE_BREAK_COMMAND)
                contents.append(SpecialNode.LINE_BREAK)
            else:
                contents.append(SpecialNode.LINE_BREAK)
                contents.append(Whitespace(' ' * env.whitespace_prefix_length))

    return Environment(name=env.name, contents=contents)


def format_recurse(nodes: Iterable[LaTeXNode], whitespace_prefix_length: int) -> Iterable[LaTeXNode]:
    child_whitespace_prefix_length = whitespace_prefix_length

    for node in nodes:
        match node:
            case SpecialNode.LINE_BREAK:
                child_whitespace_prefix_length = 0
                yield node

            case Whitespace():
                child_whitespace_prefix_length += sum(4 if sym == '\t' else 1 for sym in node.value)
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
