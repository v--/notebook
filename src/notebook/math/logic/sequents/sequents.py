from dataclasses import dataclass

from ..alphabet import AuxImproperSymbol
from ..contexts import LogicalContext


@dataclass(frozen=True)
class Sequent:
    left: LogicalContext
    right: LogicalContext

    def __str__(self) -> str:
        return f'({self.left} {AuxImproperSymbol.SEQUENT} {self.right})'

    def __repr__(self) -> str:
        return f"parse_sequent('{self}')"
