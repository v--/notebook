from collections.abc import Collection
from typing import Protocol, Self


class AbstractSubstitution[VariableT, TermT](Protocol):
    def generate_fresh_variable(self, blacklist: Collection[VariableT]) -> VariableT:
        ...

    def substitute_variable(self, var: VariableT) -> TermT:
        ...

    def modify_at(self, var: VariableT, replacement: TermT) -> Self:
        ...
