import functools
from typing import TYPE_CHECKING

from ....support.coderefs import collector
from .structure import FormalLogicStructure


if TYPE_CHECKING:
    from ..signature import SignatureMorphism


@collector.ref('def:fol_reduct_along_morphism')
def reduct_along_signature_morphism[T](morphism: SignatureMorphism, structure: FormalLogicStructure[T]) -> FormalLogicStructure[T]:
    return FormalLogicStructure(
        morphism.source,
        structure.universe,
        {sym: functools.partial(structure.apply, morphism(sym)) for sym in morphism.source},
    )
