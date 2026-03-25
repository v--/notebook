from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .terms import Term, Variable


@dataclass(frozen=True)
class TermSubstitutionSpec:
    src: Variable
    dest: Term

    def __str__(self) -> str:
        return f'{self.src} ↦ {self.dest}'

    def is_noop(self) -> bool:
        return self.src == self.dest
