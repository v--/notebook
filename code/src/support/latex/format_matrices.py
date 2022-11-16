from typing import TypeVar, Generic, cast
from dataclasses import dataclass, field

from .nodes import BracketGroup, LaTeXNode, Command, Environment, Group, Whitespace, BracelessGroup, SpecialNode
from .parser import parse_latex


T = TypeVar('T')


newline_command = Command('\\')
empty_group = BracelessGroup(contents=[])


@dataclass
class Matrix(Generic[T]):
    default: T
    payload: dict[tuple[int, int], T] = field(default_factory=dict)

    def __getitem__(self, index: tuple[int, int]):
        i, j = index
        return self.payload.get((i, j), self.default)

    def __setitem__(self, index: tuple[int, int], value: T):
        i, j = index
        self.payload[i, j] = value

    def get_height(self):
        return max(i + 1 for (i, j) in self.payload.keys())

    def get_width(self):
        return max(j + 1 for (i, j) in self.payload.keys())


def construct_environment_matrix(env: Environment) -> tuple[BracelessGroup, Matrix[BracelessGroup]]:
    i = 0
    j = 0

    matrix: Matrix[BracelessGroup] = Matrix(default=empty_group)
    buffer = BracelessGroup([])
    prefix = BracelessGroup([])

    for node in env.contents:
        if isinstance(node, BracketGroup) and len(prefix.contents) == 0 and all(isinstance(sym, Whitespace) for sym in buffer.contents):
            prefix.contents = buffer.contents + [node]
            buffer = BracelessGroup([])
        elif node == SpecialNode.ampersand:
            matrix[i, j] = buffer
            buffer = BracelessGroup([])
            j += 1
        elif node == newline_command:
            matrix[i, j] = buffer
            buffer = BracelessGroup([])
            i += 1
            j = 0
        else:
            buffer.contents.append(node)

    matrix[i, j] = buffer
    return prefix, matrix


def strip_trailing_space(grp: BracelessGroup):
    to_strip = 0

    for node in reversed(grp.contents):
        if isinstance(node, Whitespace):
            to_strip += 1
        else:
            break

    if to_strip == 0:
        return BracelessGroup(grp.contents)

    return BracelessGroup(grp.contents[:-to_strip])


def align_spaces_in_matrix(matrix: Matrix[BracelessGroup]) -> Matrix[BracelessGroup]:
    w = matrix.get_width()
    h = matrix.get_height()
    new_matrix: Matrix[BracelessGroup] = Matrix(default=empty_group)
    new_matrix[h - 1, w - 1] = empty_group  # Ensure that the size is the same

    for j in range(w):
        max_col_width = max(len(str(strip_trailing_space(matrix[i, j]))) for i in range(h))

        for i in range(h):
            stripped = strip_trailing_space(matrix[i, j])
            right_padding = max_col_width - len(str(stripped)) + 1

            if len(str(stripped)) == 0 and (j == 0 or j == w - 1):  # Too risky
                new_matrix[i, j] = matrix[i, j]
            elif max_col_width > 0:
                new_matrix[i, j] = BracelessGroup(stripped.contents + [Whitespace(' ' * right_padding)])

    return new_matrix


def matrix_to_environment(name: str, prefix: BracelessGroup, matrix: Matrix[BracelessGroup]):
    env = Environment(name=name, contents=[prefix])
    w = matrix.get_width()
    h = matrix.get_height()

    for i in range(h):
        for j in range(w - 1):
            env.contents.append(matrix[i, j])
            env.contents.append(SpecialNode.ampersand)

        if i == h - 1:
            env.contents.append(strip_trailing_space(matrix[i, w - 1]))
            env.contents.append(Whitespace('\n'))
        else:
            if len(str(matrix[i, w - 1])) == 0:
                env.contents.append(Whitespace(' '))
            else:
                env.contents.append(matrix[i, w - 1])

            env.contents.append(newline_command)

    return env


def format_recurse(node: LaTeXNode, pos: int):
    if isinstance(node, Group):
        new_grp: Group

        if isinstance(node, Environment):
            pos += 8 + len(node.name)
            new_grp = Environment(name=node.name, contents=[])
        else:
            new_grp = type(node)(contents=[])

        for child in node.contents:
            new_child = format_recurse(child, pos)
            string = str(new_child)
            nl_index = string.rfind('\n')

            if nl_index == -1:
                pos += len(string)
            else:
                pos = len(string) - nl_index - 1

            new_grp.contents.append(new_child)

        if isinstance(node, Environment):
            prefix, matrix = construct_environment_matrix(cast(Environment, new_grp))
            aligned_matrix = align_spaces_in_matrix(matrix)
            aligned_env = matrix_to_environment(node.name, prefix, aligned_matrix)
            aligned_env.contents.append(Whitespace(' ' * pos))
            return aligned_env

        return new_grp

    return node


def format_tex_matrices(string: str):
    parsed = parse_latex(string)
    new = format_recurse(parsed, pos=0)
    return str(new)
