from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .exceptions import MissingInterpretationError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from ..assertions import VariableTypeAssertion
    from .structure import HolStructureValue


@dataclass(frozen=True)
class HolVariableAssignment[T]:
    mapping: Mapping[VariableTypeAssertion, HolStructureValue[T]] = field(default_factory=dict)

    def get_value(self, assertion: VariableTypeAssertion) -> HolStructureValue[T]:
        if assertion in self.mapping:
            return self.mapping[assertion]

        raise MissingInterpretationError(f'No assignment specified for variable {assertion.term} of type {assertion.type}')

    def modify(self, assertion: VariableTypeAssertion, value: HolStructureValue[T]) -> HolVariableAssignment[T]:
        return HolVariableAssignment({**self.mapping, assertion: value})
