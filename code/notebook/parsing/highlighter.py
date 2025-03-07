from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from typing import NamedTuple


class SourcePosition(NamedTuple):
    # The offset is zero-based, the rest are one-based
    offset: int
    lineno: int
    column: int


class SpecialChars(StrEnum):
    marker = '^'
    lineno_sep = '│'
    line_break = '↵'


@dataclass
class ErrorHighlighter:
    pos_hi_start: SourcePosition
    pos_hi_end: SourcePosition

    pos_shown_start: SourcePosition
    pos_shown_end: SourcePosition

    lines_shown: Sequence[str]

    def __init__(
        self,
        source: str,
        offset_hi_start: int,
        offset_hi_end: int,
        offset_shown_start: int | None = None,
        offset_shown_end: int | None = None
    ) -> None:
        if offset_shown_start is None:
            offset_shown_start = offset_hi_start

        if offset_shown_end is None:
            offset_shown_end = offset_hi_end

        assert offset_shown_start <= offset_hi_start <= offset_hi_end <= offset_shown_end < len(source)

        lineno = 1
        column = 1
        line_start_offset = 0

        self.lines_shown = lines_shown = list[str]()

        self.pos_hi_start = SourcePosition(0, 1, 1)
        self.pos_hi_end   = SourcePosition(0, 1, 1)
        self.pos_shown_start = SourcePosition(0, 1, 1)
        self.pos_shown_end   = SourcePosition(0, 1, 1)

        for offset, char in enumerate(source):
            if offset == offset_hi_start:
                self.pos_hi_start = SourcePosition(offset, lineno, column)

            if offset == offset_hi_end:
                self.pos_hi_end = SourcePosition(offset, lineno, column)

            if offset == offset_shown_start:
                self.pos_shown_start = SourcePosition(offset, lineno, column)

            if offset == offset_shown_end:
                self.pos_shown_end = SourcePosition(offset, lineno, column)

            if char == '\n':
                if offset >= offset_shown_start:
                    lines_shown.append(source[line_start_offset:offset + 1])

                lineno += 1
                column = 1
                line_start_offset = offset + 1

                if offset >= offset_shown_end and lineno > self.pos_shown_end.lineno:
                    break
            else:
                column += 1

        if lineno <= self.pos_shown_end.lineno:
            lines_shown.append(source[line_start_offset:])

    def _iter_highlighted(self) -> Iterable[str]:
        lineno = self.pos_shown_start.lineno
        lineno_prefix_length = len(str(self.pos_shown_end.lineno))

        for line in self.lines_shown:
            yield str(lineno).ljust(lineno_prefix_length)
            yield ' ' + SpecialChars.lineno_sep + ' '

            if line[-1] == '\n':
                yield line[:-1] + SpecialChars.line_break
            else:
                yield line

            yield '\n'

            if self.pos_hi_start.lineno <= lineno <= self.pos_hi_end.lineno:
                col = self.pos_hi_start.column if lineno == self.pos_hi_start.lineno else 1
                last_col = self.pos_hi_end.column if lineno == self.pos_hi_end.lineno else len(line)

                yield ' ' * (lineno_prefix_length + 1)
                yield SpecialChars.lineno_sep
                yield ' ' * col # We must have at least one space and must subtract one from the column one-based index
                yield SpecialChars.marker * (1 + (last_col - col))
                yield '\n'

            lineno += 1

    def highlight(self) -> str:
        return ''.join(self._iter_highlighted())
