import functools
import itertools

from notebook.math.logic.signature import SignatureMorphismError
lazy from notebook.math.logic.signature import SignatureMorphism

from .structure import FormalLogicStructure


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
