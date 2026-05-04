import itertools
from dataclasses import dataclass
from typing import TYPE_CHECKING

from notebook.math.lambda_.hol import common
from notebook.math.lambda_.hol.signature import SortSymbol
from notebook.math.lambda_.types import BaseType, SimpleConnectiveType, SimpleType
from notebook.support.collections import SequentialMapping

from .exceptions import MissingInterpretationError


if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from .structure import HolStructure, HolStructureValue


@dataclass(frozen=True)
class DiscreteUnivariateFunction[T, R = T]:
    mapping: Mapping[T, R]

    def __call__(self, arg: T) -> R:
        return self.mapping[arg]


def iter_universe[T](structure: HolStructure[T], type_: SimpleType) -> Iterable[HolStructureValue[T]]:
    match type_:
        case common.prop:
            yield True
            yield False

        case BaseType() if isinstance(type_.value, SortSymbol):
            yield from structure.sort_universes[type_.value]

        case SimpleConnectiveType():
            src_values = list(iter_universe(structure, type_.left))
            dest_values = list(iter_universe(structure, type_.right))

            for codomain in itertools.combinations_with_replacement(dest_values, len(src_values)):
                yield DiscreteUnivariateFunction(SequentialMapping(zip(src_values, codomain, strict=True)))

        case _:
            raise MissingInterpretationError(f'No universe of type {type_}')
