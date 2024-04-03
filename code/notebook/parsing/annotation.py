from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Generic, TypeVar

from ..support.iteration import list_accumulator
from .tokens import AbstractToken


T_co = TypeVar('T_co', bound=AbstractToken, covariant=True)


@dataclass
class SymbolPosition:
    lineno: int
    column: int


@dataclass
class AnnotatedToken(Generic[T_co]):
    token: T_co
    start: SymbolPosition
    end: SymbolPosition


@list_accumulator
def annotate_existing_tokens(seq: Sequence[T_co]) -> Iterable[AnnotatedToken[T_co]]:
    """Take a sequence of tokens and add positional annotation.
    We assume that their string representation is accurate."""

    lineno = 1
    column = 1

    for _i, token in enumerate(seq):
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
