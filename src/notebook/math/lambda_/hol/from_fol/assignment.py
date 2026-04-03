from typing import TYPE_CHECKING

from ...assertions import VariableTypeAssertion
from ...terms import Variable as HolVariable
from .. import common
from ..structure import HolVariableAssignment


if TYPE_CHECKING:
    from ....logic.structure import VariableAssignment as FolVariableAssignment


def fol_assignment_to_hol_assignment[T](fol_assignment: FolVariableAssignment[T]) -> HolVariableAssignment[T]:
    return HolVariableAssignment[T]({
        VariableTypeAssertion(HolVariable(var.identifier), common.individual): value
        for var, value in fol_assignment.mapping.items()
    })
