from dataclasses import dataclass, field
from typing import TYPE_CHECKING, overload

from notebook.math.lambda_.assertions import VariableTypeAssertion

from .exceptions import MissingInterpretationError


if TYPE_CHECKING:
    from collections.abc import Mapping

    from notebook.math.lambda_.terms import Variable
    from notebook.math.lambda_.types import SimpleType

    from .structure import HolStructureValue


@dataclass(frozen=True)
class HolVariableAssignment[T]:
    mapping: Mapping[VariableTypeAssertion, HolStructureValue[T]] = field(default_factory=dict)

    def _get_value_assertion(self, assertion: VariableTypeAssertion) -> HolStructureValue[T]:
        if assertion in self.mapping:
            return self.mapping[assertion]

        raise MissingInterpretationError(f'No assignment specified for variable {assertion.term} of type {assertion.type}')

    def _get_value_var_type(self, var: Variable, type_: SimpleType) -> HolStructureValue[T]:
        return self._get_value_assertion(VariableTypeAssertion(var, type_))

    @overload
    def get_value(self, assertion: VariableTypeAssertion) -> HolStructureValue[T]: ...
    @overload
    def get_value(self, var: Variable, type_: SimpleType) -> HolStructureValue[T]: ...
    def get_value(self, *args, **kwargs) -> HolStructureValue[T]:
        if len(args) + len(kwargs) == 1:
            return self._get_value_assertion(*args, **kwargs)

        return self._get_value_var_type(*args, **kwargs)

    def _modify_assertion(self, assertion: VariableTypeAssertion, value: HolStructureValue[T]) -> HolVariableAssignment[T]:
        return HolVariableAssignment({**self.mapping, assertion: value})

    def _modify_var_type(self, var: Variable, type_: SimpleType, value: HolStructureValue[T]) -> HolVariableAssignment[T]:
        return self._modify_assertion(VariableTypeAssertion(var, type_), value)

    @overload
    def modify(self, assertion: VariableTypeAssertion, value: HolStructureValue[T]) -> HolVariableAssignment[T]: ...
    @overload
    def modify(self, var: Variable, type_: SimpleType, value: HolStructureValue[T]) -> HolVariableAssignment[T]: ...
    def modify(self, *args, **kwargs) -> HolVariableAssignment[T]:
        if len(args) + len(kwargs) == 2:
            return self._modify_assertion(*args, **kwargs)

        return self._modify_var_type(*args, **kwargs)
