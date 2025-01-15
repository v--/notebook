from collections.abc import Collection
from typing import NamedTuple


class STTSignature(NamedTuple):
    base_types: Collection[str]
    constant_terms: Collection[str]


EMPTY_SIGNATURE = STTSignature(base_types=set(), constant_terms=set())
PLAIN_TYPED_SIGNATURE = STTSignature(base_types={'o', 'ι'}, constant_terms=set())
PROP_TYPED_SIGNATURE = STTSignature(base_types={'o', 'ι'}, constant_terms={'Q', 'I'})
