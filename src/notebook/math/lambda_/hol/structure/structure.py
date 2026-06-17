from dataclasses import dataclass
from typing import Protocol
lazy from collections.abc import Collection, Mapping

lazy from notebook.math.lambda_.hol.signature import HolSignature, NonLogicalConstantSymbol, SortSymbol


# We should wait for a further development, e.g. PEP 827, so that we can introduce better typing here.
class HolStructureValue[T](Protocol):
    pass


@dataclass
class HolStructure[T]:
    signature: HolSignature
    sort_universes: Mapping[SortSymbol, Collection[T]]
    interpretation: Mapping[NonLogicalConstantSymbol, HolStructureValue[T]]
