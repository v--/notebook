from dataclasses import dataclass

from ..alphabet import AuxImproperSymbol
from ..contexts import LogicalContextSchema


@dataclass(frozen=True)
class SequentSchema:
    left: LogicalContextSchema
    right: LogicalContextSchema

    def __str__(self) -> str:
        return f'({self.left} {AuxImproperSymbol.SEQUENT} {self.right})'

    def __repr__(self) -> str:
        return f"parse_sequent_schema('{self}')"
