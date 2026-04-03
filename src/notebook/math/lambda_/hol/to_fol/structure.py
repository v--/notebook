import functools
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .....exceptions import UnreachableException
from .....support.coderefs import collector
from ....logic.signature import SignatureSymbol
from ....logic.structure import FormalLogicStructure
from ...alphabet import BinaryTypeConnective
from ...types import BaseType, SimpleConnectiveType, SimpleType
from .. import common
from ..structure import HolStructureValue, iter_universe
from ..type_features import extract_bound_types, get_subtypes
from .signature import hol_signature_to_fol


if TYPE_CHECKING:
    from ..expression import HolExpression
    from ..signature import NonLogicalConstantSymbol
    from ..structure import HolStructure


@dataclass
class FolTranslatedStructure[T](FormalLogicStructure[HolStructureValue[T]]):
    hol_structure: HolStructure[T]

    def check_type(self, type_: SimpleType, value: HolStructureValue[T]) -> bool:
        return any(value == ref_value for ref_value in iter_universe(self.hol_structure, type_))

    # We do not make type checks because there is no good way to compare functions in Python
    def _apply_curried_recurse(
        self,
        type_: SimpleType,
        value: HolStructureValue[T],
        *args: HolStructureValue[T],
    ) -> HolStructureValue[T]:
        match type_:
            case BaseType():
                return value

            case SimpleConnectiveType() if callable(value):
                arg, *rest = args
                new_value = value(arg)
                return self._apply_curried_recurse(type_.right, new_value, *rest)

            case _:
                raise UnreachableException

    def apply_var(
        self,
        type_: SimpleType,
        value: HolStructureValue[T],
        *args: HolStructureValue[T],
    ) -> HolStructureValue[T]:
        return self._apply_curried_recurse(type_, value, *args)

    def apply_nl_const(
        self,
        sym: NonLogicalConstantSymbol,
        *args: HolStructureValue[T],
    ) -> HolStructureValue[T]:
        return self._apply_curried_recurse(sym.type, self.hol_structure.interpretation[sym], *args)


def iter_expression_types[T](
    hol_structure: HolStructure[T],
    hol_expression: HolExpression,
) -> Iterable[SimpleType]:
    yield common.prop
    yield SimpleConnectiveType(BinaryTypeConnective.ARROW, common.prop, common.prop)
    yield SimpleConnectiveType(
        BinaryTypeConnective.ARROW,
        common.prop,
        SimpleConnectiveType(BinaryTypeConnective.ARROW, common.prop, common.prop),
    )

    for sort in hol_structure.signature.iter_sorts():
        yield BaseType(sort)

    for nl_sym in hol_structure.signature.iter_nonlogical():
        yield from get_subtypes(nl_sym.type)

    for type_ in extract_bound_types(hol_expression.term):
        yield from get_subtypes(type_)


@collector.ref('alg:hol_to_fol/structure')
def hol_structure_to_fol[T](
    hol_structure: HolStructure[T],
    hol_expression: HolExpression,
) -> FolTranslatedStructure[T]:
    translated_signature = hol_signature_to_fol(hol_structure.signature, hol_expression)
    universe = list[HolStructureValue[T]]()
    interpretation = dict[SignatureSymbol, Callable[..., HolStructureValue[T]] | Callable[..., bool]]()

    for type_ in iter_expression_types(hol_structure, hol_expression):
        universe.extend(iter_universe(hol_structure, type_))

    translated_structure = FolTranslatedStructure(
        translated_signature,
        universe,
        interpretation,
        hol_structure,
    )

    for type_, pred_sym in translated_signature.type_predicates.items():
        interpretation[pred_sym] = functools.partial(translated_structure.check_type, type_)

    for (type_, _), app_sym in translated_signature.type_appliers.items():
        interpretation[app_sym] = functools.partial(translated_structure.apply_var, type_)

    for (nl_sym, _), fol_sym in translated_signature.nl_constant_map.items():
        interpretation[fol_sym] = functools.partial(translated_structure.apply_nl_const, nl_sym)

    return translated_structure
