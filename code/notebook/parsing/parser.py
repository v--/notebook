from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from .exceptions import ParsingError
from .highlighter import ErrorHighlighter
from .tokens import AbstractToken


T_co = TypeVar('T_co', bound=AbstractToken, covariant=True)


@dataclass
class Parser(Generic[T_co]):
    seq: Sequence[T_co]
    index: int = field(default=0, init=False)

    def reset(self) -> None:
        self.index = 0

    def is_at_end(self) -> bool:
        return self.index == len(self.seq)

    def advance(self, count: int = 1) -> None:
        assert 0 <= self.index + count <= len(self.seq)
        self.index += count

    def peek(self) -> T_co:
        if self.is_at_end():
            raise self.error('Unexpected end of input')

        return self.seq[self.index]

    def peek_multiple(self, count: int) -> Sequence[T_co]:
        return self.seq[self.index: self.index + count]

    def assert_exhausted(self) -> None:
        if not self.is_at_end():
            raise self.error('Finished parsing but there is still input left')

    def error(self, message: str, i_first_token: int | None = None, i_last_token: int | None = None) -> ParsingError:
        err = ParsingError(message)

        if len(self.seq) == 0:
            return err

        # It is possible that the index is past the end of the input
        adjusted_index = min(self.index, len(self.seq) - 1)

        highlighter = ErrorHighlighter(
            self.seq,
            i_first_token if i_first_token is not None else adjusted_index,
            i_last_token if i_last_token is not None else adjusted_index,
        )

        err.add_note(highlighter.highlight())
        return err
