from collections.abc import Collection
from typing import Protocol, Self


class AbstractAtomicSubstitution[VariableT, ReplacementT](Protocol):
    def generate_fresh_variable(self, blacklist: Collection[VariableT]) -> VariableT:
        ...

    def substitute_variable(self, var: VariableT) -> ReplacementT:
        ...

    def modify_at(self, var: VariableT, replacement: ReplacementT) -> Self:
        ...
