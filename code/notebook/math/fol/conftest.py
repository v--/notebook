import pytest

from ...support.unicode import itoa_subscripts
from .signature import FOLSignature


@pytest.fixture()
def empty_signature() -> FOLSignature:
    return FOLSignature()


@pytest.fixture()
def dummy_signature(max_args: int = 10) -> FOLSignature:
    signature = FOLSignature()

    for l in ['F', 'G', 'H', 'T']:
        for i in range(max_args):
            signature.add_function_symbol(l + itoa_subscripts(i), arity=i)

    for l in ['P', 'Q', 'R', 'S']:
        for i in range(max_args):
            signature.add_predicate_symbol(l + itoa_subscripts(i), arity=i)

    return signature
