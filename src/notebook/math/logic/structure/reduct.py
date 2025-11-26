import functools

from ..signature import SignatureMorphism
from .structure import FormalLogicStructure


# This is def:fol_structure_reduct in the monograph
def reduct_along_signature_morphism[T](morphism: SignatureMorphism, structure: FormalLogicStructure[T]) -> FormalLogicStructure[T]:
    return FormalLogicStructure(
        morphism.source,
        structure.universe,
        {sym: functools.partial(structure.apply, morphism(sym)) for sym in morphism.source}
    )
