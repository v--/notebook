from collections.abc import Iterator, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Phrase:
    words: Sequence[str]

    def __str__(self) -> str:
        return ' '.join(self.words)

    def __iter__(self) -> Iterator[str]:
        return iter(self.words)

    def __len__(self) -> int:
        return len(self.words)

    def __hash__(self) -> int:
        return hash(tuple(self.words))
