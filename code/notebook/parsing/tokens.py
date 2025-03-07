from typing import NamedTuple


class Token[TokenKindT](NamedTuple):
    kind: TokenKindT
    value: str
    offset: int

    @property
    def end_offset(self) -> int:
        return self.offset + len(self.value)
