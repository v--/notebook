from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from types import TracebackType
from typing import Self

from .exceptions import ParsingError
from .highlighter import ErrorHighlighter
from .tokens import AbstractToken


@dataclass
class Parser[T: AbstractToken]:
    seq: Sequence[T]
    index: int = field(default=0, init=False)

    def gobble_iter(self, predicate: Callable[[T], bool]) -> Iterable[T]:
        while not self.is_at_end() and predicate(head := self.peek()):
            yield head
            self.advance()

    def gobble_list(self, predicate: Callable[[T], bool]) -> Sequence[T]:
        return list(self.gobble_iter(predicate))

    def gobble_string(self, predicate: Callable[[T], bool]) -> str:
        return ''.join(str(x) for x in self.gobble_iter(predicate))

    def gobble_and_skip(self, predicate: Callable[[T], bool]) -> None:
        for _ in self.gobble_iter(predicate):
            pass

    def reset(self) -> None:
        self.index = 0

    def is_at_end(self) -> bool:
        return self.index == len(self.seq)

    def advance(self, count: int = 1) -> None:
        assert 0 <= self.index + count <= len(self.seq)
        self.index += count

    def peek(self) -> T:
        if self.is_at_end():
            raise self.error('Unexpected end of input')

        return self.seq[self.index]

    def peek_multiple(self, count: int) -> Sequence[T]:
        return self.seq[self.index: self.index + count]

    def assert_exhausted(self) -> None:
        if not self.is_at_end():
            raise self.error('Finished parsing but there is still input left')

    def error(
        self,
        message: str,
        i_first_token: int | None = None,
        i_last_token: int | None = None,
        i_first_visible_token: int | None = None,
        i_last_visible_token: int | None = None
    ) -> ParsingError:
        err = ParsingError(message)

        if len(self.seq) == 0:
            return err

        # It is possible that the index is past the end of the input
        adjusted_index = min(self.index, len(self.seq) - 1)

        if i_first_token is None:
            i_first_token = adjusted_index

        if i_last_token is None:
            i_last_token = adjusted_index

        highlighter = ErrorHighlighter(
            self.seq,
            i_first_token,
            i_last_token,
            i_first_visible_token if i_first_visible_token is not None else i_first_token,
            i_last_visible_token if i_last_visible_token is not None else i_last_token,
        )

        err.add_note(highlighter.highlight())
        return err

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
     ) -> None:
        if exc_type is None:
            self.assert_exhausted()
