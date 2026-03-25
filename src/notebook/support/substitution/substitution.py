from typing import TYPE_CHECKING, Protocol, Self


if TYPE_CHECKING:
    from collections.abc import Collection


class AbstractAtomicSubstitution[VariableT, ReplacementT](Protocol):
    def generate_fresh_variable(self, blacklist: Collection[VariableT]) -> VariableT:
        ...

    def substitute_variable(self, var: VariableT) -> ReplacementT:
        ...

    def modify_at(self, var: VariableT, replacement: ReplacementT) -> Self:
        ...
