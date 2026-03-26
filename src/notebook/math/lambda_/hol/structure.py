from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from collections.abc import Collection, Mapping

    from .signature import HolSignature
    from .symbols import NonLogicalConstantSymbol, SortSymbol


# We should wait for a further development, e.g. PEP 827, so that we can introduce better typing here.
class HolStructureValue[T](Protocol):
    pass


@dataclass
class HolStructure[T]:
    signature: HolSignature
    sort_universes: Mapping[SortSymbol, Collection[T]]
    interpretation: Mapping[NonLogicalConstantSymbol, HolStructureValue[T]]
