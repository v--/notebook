from typing import NamedTuple


class FunctionSymbol(NamedTuple):
    name: str
    arity: int


class PredicateSymbol(NamedTuple):
    name: str
    arity: int


class FOLSignature(NamedTuple):
    function_symbols: list[FunctionSymbol]
    predicate_symbols: list[PredicateSymbol]
