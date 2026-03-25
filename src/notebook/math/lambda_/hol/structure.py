from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from collections.abc import Callable, Collection, Mapping

    from .signature import HolSignature
    from .symbols import NonLogicalConstantSymbol, SortSymbol


@dataclass
class HolStructure[T]:
    signature: HolSignature
    frame: Mapping[SortSymbol, Collection[T]]
    interpretation: Mapping[NonLogicalConstantSymbol, T | Callable[[T], Any]]
