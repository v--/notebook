import functools
from typing import TYPE_CHECKING

from notebook.math.lambda_.hol.alphabet import SortName
from notebook.math.lambda_.hol.structure import HolStructure, HolStructureValue
from notebook.support.coderefs import collector

from .signature import fol_signature_to_hol_signature


if TYPE_CHECKING:
    from notebook.math.logic.signature import SignatureSymbol
    from notebook.math.logic.structure import FormalLogicStructure


def _curry_fol_interpretation[T](fol_structure: FormalLogicStructure[T], sym: SignatureSymbol, *args: T) -> HolStructureValue[T]:
    if sym.arity == len(args):
        interp = fol_structure.interpretation[sym]
        return interp(*args) if callable(interp) else interp

    return functools.partial(_curry_fol_interpretation, fol_structure, sym, *args)


@collector.ref('alg:fol_to_hol/structure')
def fol_structure_to_hol_structure[T](fol_structure: FormalLogicStructure[T]) -> HolStructure[T]:
    hol_signature = fol_signature_to_hol_signature(fol_structure.signature)

    return HolStructure(
        signature=hol_signature,
        sort_universes={hol_signature.get_sort_symbol(SortName.INDIVIDUAL): fol_structure.universe},
        interpretation={
            hol_signature.get_nonlogical_constant_symbol(sym.name): _curry_fol_interpretation(fol_structure, sym)
            for sym in fol_structure.signature
        },
    )
