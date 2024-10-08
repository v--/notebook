from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from enum import StrEnum

from ..support.iteration import string_accumulator
from .annotation import AnnotatedToken, annotate_existing_tokens
from .tokens import AbstractToken


class SpecialChars(StrEnum):
    marker = '^'
    lineno_sep = '│'
    line_break = '↵'


@dataclass
class ErrorHighlighter[T: AbstractToken]:
    seq: Sequence[T]
    i_first_token: int
    i_last_token: int
    i_first_visible_token: int
    i_last_visible_token: int
    special: type[SpecialChars] = SpecialChars
    annotated: Sequence[AnnotatedToken[T]] = field(init=False)

    def __post_init__(self) -> None:
        assert 0 <= self.i_first_visible_token <= self.i_first_token <= self.i_last_token <= self.i_last_visible_token < len(self.seq)
        self.annotated = annotate_existing_tokens(self.seq)

    def _get_i_first_drawn_token(self) -> int:
        return min(
            (i for i, atoken in enumerate(self.annotated) if atoken.end.lineno == self.annotated[self.i_first_visible_token].end.lineno),
            default=0
        )

    def _get_i_last_drawn_token(self) -> int:
        return max(
            (i for i, atoken in enumerate(self.annotated) if atoken.end.lineno == self.annotated[self.i_last_visible_token].end.lineno),
            default=len(self.annotated) - 1
        )

    def _iter_tokens_in_range(self) -> Iterable[AnnotatedToken[T]]:
        for i in range(self.i_first_token, self.i_last_token + 1):
            yield self.annotated[i]

    def _highlight_line(self, lineno: int, lineno_prefix_length: int) -> Iterable[str]:
        yield str(lineno).ljust(lineno_prefix_length)
        yield ' ' + self.special.lineno_sep + ' '

        for _i, atoken in enumerate(self.annotated):
            if atoken.end.lineno == lineno:
                value = str(atoken.token)
                lines = value.splitlines(keepends=True)
                yield lines[-1].replace('\n', self.special.line_break)

            elif atoken.start.lineno == lineno:
                value = str(atoken.token)
                lines = value.splitlines(keepends=True)
                yield lines[0].replace('\n', self.special.line_break)

        yield '\n'

        # The columns are one-based, so we subtract 1
        try:
            first_col = -1 + min(
                atoken.start.column for atoken in self._iter_tokens_in_range() if atoken.start.lineno == lineno
            )
        except ValueError:
            return

        last_col = -1 + max(
            atoken.end.column for atoken in self._iter_tokens_in_range() if atoken.end.lineno == lineno
        )

        yield ' ' * (lineno_prefix_length + 1)
        yield self.special.lineno_sep
        yield ' ' * (1 + first_col)
        yield self.special.marker * (last_col - first_col)
        yield '\n'

    @string_accumulator()
    def highlight(self) -> Iterable[str]:
        first_lineno = self.annotated[self._get_i_first_drawn_token()].start.lineno
        last_lineno = self.annotated[self._get_i_last_drawn_token()].end.lineno

        lineno_prefix_length = len(str(last_lineno))

        for lineno in range(first_lineno, last_lineno + 1):
            yield from self._highlight_line(lineno, lineno_prefix_length)
