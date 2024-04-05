import pytest

from ...support.subscripts import itoa_subscripts
from .signature import FOLSignature, FunctionSymbol, PredicateSymbol


@pytest.fixture()
def empty_signature() -> FOLSignature:
    return FOLSignature(
        function_symbols=[],
        predicate_symbols=[]
    )


@pytest.fixture()
def dummy_signature(max_args: int = 10) -> FOLSignature:
    return FOLSignature(
        function_symbols=[
            FunctionSymbol(l + itoa_subscripts(i), arity=i)
            for i in range(max_args)
            for l in ['f', 'g', 'h', 't']
        ],
        predicate_symbols=[
            PredicateSymbol(l + itoa_subscripts(i), arity=i)
            for i in range(max_args)
            for l in ['p', 'q', 'r', 's']
        ]
    )


@pytest.fixture()
def propositional_signature() -> FOLSignature:
    return FOLSignature(
        function_symbols=[],
        predicate_symbols=[
            PredicateSymbol(l, arity=0)
            for l in 'abcdefghijklmnopqrstuvwxyz'
        ]
    )
