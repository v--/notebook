import random
from typing import TYPE_CHECKING

from notebook.math.lambda_.hol.structure import evaluate_hol_expression
from notebook.math.lambda_.parsing import parse_typed_term
from notebook.math.logic.parsing import parse_formula
from notebook.math.logic.structure import VariableAssignment as FolVariableAssignment
from notebook.math.logic.structure import evaluate_formula
from notebook.math.logic.variables import get_formula_free_variables
from notebook.math.rings.modular import Z3
from notebook.support.pytest import pytest_parametrize_kwargs

from .assignment import fol_assignment_to_hol_assignment
from .formula import fol_formula_to_hol_expression


if TYPE_CHECKING:
    from notebook.math.lambda_.hol.structure import HolStructure
    from notebook.math.logic.structure import FormalLogicStructure


@pytest_parametrize_kwargs(
    dict(fol_formula='⊤', hol_term='L⊤'),
    dict(fol_formula='(x ≤ y)', hol_term='((≤x)y)'),
    dict(fol_formula='((x + y) ≤ z)', hol_term='((≤((+x)y))z)'),
    dict(fol_formula='¬(x ≤ y)', hol_term='(L¬((≤x)y))'),
    dict(fol_formula='(⊤ ∧ ⊥)', hol_term='((L∧L⊤)L⊥)'),
    dict(fol_formula='∀x.∃y.(x ≤ y)', hol_term='(L∀(λx:ι.(L∃(λy:ι.((≤x)y)))))'),
)
def test_fol_symbol_to_hol_type(
    fol_formula: str,
    hol_term: str,
    fol_z3_model: FormalLogicStructure[Z3],
    hol_z3_model: HolStructure,
) -> None:
    fol_formula_ = parse_formula(fol_formula, fol_z3_model.signature)
    hol_term_ = parse_typed_term(hol_term, hol_z3_model.signature)

    result = fol_formula_to_hol_expression(fol_z3_model.signature, fol_formula_)
    assert result.term == hol_term_

    fol_assignment = FolVariableAssignment[Z3]({
        var: random.choice(list(fol_z3_model.universe)) for var in get_formula_free_variables(fol_formula_)
    })

    hol_assignment = fol_assignment_to_hol_assignment(fol_assignment)

    assert evaluate_formula(fol_formula_, fol_z3_model, fol_assignment) == evaluate_hol_expression(result, hol_z3_model, hol_assignment)
