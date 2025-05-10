from collections.abc import Collection, Iterable
from enum import StrEnum
from typing import NamedTuple, cast

from ..support.iteration import dict_accumulator
from .exceptions import InvalidTokenError


class Token[TokenKindT](NamedTuple):
    kind: TokenKindT
    value: str
    offset: int

    @property
    def end_offset(self) -> int:
        return self.offset + len(self.value)


@dict_accumulator
def map_of_str_enum_to_tokens[TokenKindT](allowed_token_kinds: Collection[TokenKindT], enum: type[StrEnum]) -> Iterable[tuple[str, TokenKindT]]:
    for entry in enum:
        if entry.name not in allowed_token_kinds:
            raise InvalidTokenError(f'Entry {entry.name} is not recognized')

        yield entry.value, cast('TokenKindT', entry.name)


@dict_accumulator
def map_of_str_enum_to_single_token[TokenKindT](token_kind: TokenKindT, enum: type[StrEnum]) -> Iterable[tuple[str, TokenKindT]]:
    for entry in enum:
        yield entry.value, token_kind
