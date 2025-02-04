from collections.abc import Collection
from dataclasses import dataclass


@dataclass(frozen=True)
class LambdaSignature:
    base_types: Collection[str]
    constant_terms: Collection[str]


EMPTY_SIGNATURE = LambdaSignature(base_types=set(), constant_terms=set())
