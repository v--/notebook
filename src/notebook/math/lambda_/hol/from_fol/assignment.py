from typing import TYPE_CHECKING

from notebook.math.lambda_.assertions import VariableTypeAssertion
from notebook.math.lambda_.hol import common
from notebook.math.lambda_.hol.structure import HolVariableAssignment
from notebook.math.lambda_.terms import Variable as HolVariable


if TYPE_CHECKING:
    from notebook.math.logic.structure import VariableAssignment as FolVariableAssignment


def fol_assignment_to_hol_assignment[T](fol_assignment: FolVariableAssignment[T]) -> HolVariableAssignment[T]:
    return HolVariableAssignment[T]({
        VariableTypeAssertion(HolVariable(var.identifier), common.individual): value
        for var, value in fol_assignment.mapping.items()
    })
