from typing import TYPE_CHECKING

from ..signature import common_types
from ..structure import HolStructure, HolStructureValue
from .signature import fol_signature_to_hol_signature


if TYPE_CHECKING:
    from ....logic.signature import SignatureSymbol
    from ....logic.structure import FormalLogicStructure


def _curry_fol_interpretation[T](fol_structure: FormalLogicStructure[T], sym: SignatureSymbol, *args: T) -> HolStructureValue[T]:
    if sym.arity == len(args):
        interp = fol_structure.interpretation[sym]
        return interp(*args) if callable(interp) else interp

    return lambda a: _curry_fol_interpretation(fol_structure, sym, *args, a)


# alg:fol_structure_to_hol_structure
def fol_structure_to_hol_structure[T](fol_structure: FormalLogicStructure[T]) -> HolStructure[T]:
    hol_signature = fol_signature_to_hol_signature(fol_structure.signature)

    return HolStructure(
        signature=hol_signature,
        sort_universes={common_types.individual: fol_structure.universe},
        interpretation={
            hol_signature.get_nonlogical_constant_symbol(sym.name): _curry_fol_interpretation(fol_structure, sym)
            for sym in fol_structure.signature
        },
    )
