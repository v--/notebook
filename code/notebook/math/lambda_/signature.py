from collections.abc import Collection
from typing import NamedTuple


class LambdaSignature(NamedTuple):
    base_types: Collection[str]
    constant_terms: Collection[str]


EMPTY_SIGNATURE = LambdaSignature(base_types=set(), constant_terms=set())
