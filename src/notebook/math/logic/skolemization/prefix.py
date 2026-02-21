from collections.abc import Iterator
from dataclasses import dataclass, field

from ..alphabet import Quantifier
from ..terms import Variable


@dataclass(frozen=True)
class QuantifierPrefix:
    payload: list[tuple[Quantifier, Variable]] = field(default_factory=list)

    def append(self, quant: Quantifier, var: Variable) -> None:
        self.payload.append((quant, var))

    def __len__(self) -> int:
        return len(self.payload)

    def __iter__(self) -> Iterator[tuple[Quantifier, Variable]]:
        return iter(self.payload)

    def is_universal(self) -> bool:
        return all(quant == Quantifier.UNIVERSAL for quant, var in self.payload)

    def is_existential(self) -> bool:
        return all(quant == Quantifier.EXISTENTIAL for quant, var in self.payload)
