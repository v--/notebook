from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import overload

from ...parsing.whitespace import Whitespace
from ...support.iteration import get_strip_slice
from .tokens import TextToken


class TokenSequence(Sequence[TextToken]):
    tokens: Sequence[TextToken]

    def __init__(self, tokens: Iterable[TextToken] | None = None) -> None:
        if tokens is None:
            self.tokens = []
        else:
            self.tokens = list(tokens)

    def __len__(self) -> int:
        return len(self.tokens)

    @overload
    def __getitem__(self, i: int) -> TextToken: ...
    @overload
    def __getitem__(self, i: slice) -> 'TokenSequence': ...
    def __getitem__(self, i: int | slice) -> 'TextToken | TokenSequence':
        if isinstance(i, slice):
            return TokenSequence(self.tokens[i])

        return self.tokens[i]

    def __iter__(self) -> Iterator[TextToken]:
        return iter(self.tokens)

    def __str__(self) -> str:
        return ''.join(map(str, self))

    def __reversed__(self) -> Iterator[TextToken]:
        return iter(self[::-1])

    def __hash__(self) -> int:
        return hash(tuple(self.tokens))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenSequence):
            return NotImplemented

        return self.tokens == other.tokens

    def strip(self) -> 'TokenSequence':
        return self[get_strip_slice(self, lambda token: isinstance(token, Whitespace))]

    def split_by(self, predicate: Callable[[TextToken], bool], *, strip: bool = True) -> 'Iterable[TokenSequence]':
        last_split = 0

        for i, token in enumerate(self.tokens):
            if predicate(token):
                seq = TokenSequence(self.tokens[last_split:i])
                adjusted = seq.strip() if strip else seq

                if len(adjusted) > 0:
                    yield adjusted

                last_split = i + 1

        if len(self) > 0 and not predicate(self.tokens[-1]):
            seq = TokenSequence(self.tokens[last_split:])
            adjusted = seq.strip() if strip else seq

            if len(adjusted) > 0:
                yield adjusted
