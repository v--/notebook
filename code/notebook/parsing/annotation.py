from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from ..support.iteration import list_accumulator
from .old_tokens import AbstractToken


@dataclass(frozen=True)
class SymbolPosition:
    lineno: int
    column: int


@dataclass(frozen=True)
class AnnotatedToken[T: AbstractToken]:
    token: T
    start: SymbolPosition
    end: SymbolPosition


@list_accumulator
def annotate_existing_tokens[T: AbstractToken](seq: Sequence[T]) -> Iterable[AnnotatedToken[T]]:
    """Take a sequence of tokens and add positional annotation.
    We assume that their string representation is accurate."""

    lineno = 1
    column = 1

    for token in seq:
        start = SymbolPosition(lineno, column)
        end: SymbolPosition

        for sym in str(token):
            if sym == '\n':
                end = SymbolPosition(lineno, column + 1)
                column = 1
                lineno += 1
            else:
                column += 1
                end = SymbolPosition(lineno, column)

        yield AnnotatedToken(token, start, end)
