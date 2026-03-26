from typing import TYPE_CHECKING

from ...assertions import VariableTypeAssertion
from ...terms import Variable as HolVariable
from ...types import BaseType
from ..assignment import HolVariableAssignment
from ..symbols import common_types


if TYPE_CHECKING:
    from ....logic.structure import VariableAssignment as FolVariableAssignment


def fol_assignment_to_hol_assignment[T](fol_assignment: FolVariableAssignment[T]) -> HolVariableAssignment[T]:
    return HolVariableAssignment[T]({
        VariableTypeAssertion(HolVariable(var.identifier), BaseType(common_types.individual)): value
        for var, value in fol_assignment.mapping.items()
    })
