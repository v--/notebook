from collections.abc import Collection

from ..signature import FormalLogicSignature, SignatureSymbol
from ..signature_translation import SignatureMorphism
from .structure import FormalLogicStructure


# This is def:fol_structure_reduct in the monograph
def reduct_along_signature_morphism[T](morphism: SignatureMorphism, structure: FormalLogicStructure[T]) -> FormalLogicStructure[T]:
    class StructureReduct:
        universe: Collection[T]
        signature: FormalLogicSignature

        def __init__(self) -> None:
            self.universe = structure.universe
            self.signature = structure.signature

        def apply_function(self, f: SignatureSymbol, *args: T) -> T:
            return structure.apply_function(morphism.mapping[f], *args)

        def apply_predicate(self, p: SignatureSymbol, *args: T) -> bool:
            return structure.apply_predicate(morphism.mapping[p], *args)

    return StructureReduct()
