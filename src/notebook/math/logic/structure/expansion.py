import functools
import itertools
from typing import TYPE_CHECKING

from notebook.math.logic.signature import SignatureMorphismError

from .structure import FormalLogicStructure


if TYPE_CHECKING:
    from notebook.math.logic.signature import SignatureMorphism


def expand_along_signature_morphism[T](morphism: SignatureMorphism, structure: FormalLogicStructure[T]) -> FormalLogicStructure[T]:
    for i, a in enumerate(morphism.source):
        for b in itertools.islice(morphism.source, i + 1, None):
            if morphism(a) == morphism(b):
                raise SignatureMorphismError(f'Conflict between {a} and {b}: both map to {morphism(a)}')

    return FormalLogicStructure(
        morphism.get_modified_signature(),
        structure.universe,
        {morphism(sym): functools.partial(structure.apply, sym) for sym in morphism.source},
    )
