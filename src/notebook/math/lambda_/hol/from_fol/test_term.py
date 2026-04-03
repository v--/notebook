import random
from typing import TYPE_CHECKING

from .....support.pytest import pytest_parametrize_kwargs
from ....logic.parsing import parse_term
from ....logic.structure import VariableAssignment as FolVariableAssignment
from ....logic.structure import evaluate_term
from ....logic.variables import get_term_variables
from ....rings.modular import Z3
from ...parsing import parse_typed_term
from ..structure import evaluate_hol_expression
from .assignment import fol_assignment_to_hol_assignment
from .term import fol_term_to_hol_expression


if TYPE_CHECKING:
    from ....logic.structure import FormalLogicStructure
    from ..structure import HolStructure


@pytest_parametrize_kwargs(
    dict(fol_term='0', hol_term='0'),
    dict(fol_term='S⁺x', hol_term='(S⁺x)'),
    dict(fol_term='(x + y)', hol_term='((+x)y)'),
)
def test_fol_symbol_to_hol_type(
    fol_term: str,
    hol_term: str,
    fol_z3_model: FormalLogicStructure,
    hol_z3_model: HolStructure,
) -> None:
    fol_term_ = parse_term(fol_term, fol_z3_model.signature)
    hol_term_ = parse_typed_term(hol_term, hol_z3_model.signature)

    result = fol_term_to_hol_expression(fol_z3_model.signature, fol_term_)
    assert result.term == hol_term_

    fol_assignment = FolVariableAssignment[Z3]({
        var: random.choice(list(fol_z3_model.universe)) for var in get_term_variables(fol_term_)
    })

    hol_assignment = fol_assignment_to_hol_assignment(fol_assignment)

    assert evaluate_term(fol_term_, fol_z3_model, fol_assignment) == evaluate_hol_expression(result, hol_z3_model, hol_assignment)
