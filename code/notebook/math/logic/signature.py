from collections.abc import Iterable, MutableMapping


class FormalLogicSignature:
    '''What we call here function and predicate symbols can have multiple Unicode graphemes,
    yet they are guaranteed to correspond to one lexeme ("token").
    This makes it more convenient to use at the cost of possibly confusing terminology.
    Calling them "symbols" corresponds to their usage in the literature, where Unicode is not involved.'''

    _payload: MutableMapping[str, int]

    def __init__(self) -> None:
        self._payload = {}

    def add_function_symbol(self, name: str, arity: int) -> None:
        assert not self.is_function_symbol(name)
        self._payload[name] = arity

    def add_predicate_symbol(self, name: str, arity: int) -> None:
        assert not self.is_predicate_symbol(name)
        self._payload[name] = -1 - arity

    def is_function_symbol(self, name: str) -> bool:
        return self._payload.get(name, -1) >= 0

    def is_predicate_symbol(self, name: str) -> bool:
        return self._payload.get(name, 0) < 0

    def get_function_arity(self, name: str) -> int:
        assert self.is_function_symbol(name)
        return self._payload[name]

    def get_predicate_arity(self, name: str) -> int:
        assert self.is_predicate_symbol(name)
        return -1 - self._payload[name]

    def iter_function_symbols(self) -> Iterable[str]:
        return sorted(sym for sym, arity in self._payload.items() if arity >= 0)

    def iter_predicate_symbols(self) -> Iterable[str]:
        return sorted(sym for sym, arity in self._payload.items() if arity < 0)


EMPTY_SIGNATURE = FormalLogicSignature()
