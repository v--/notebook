import itertools
from typing import TYPE_CHECKING, cast

from .. import common
from ..theories.arithmetic import ARITHMETIC_SIGNATURE as HOL_ARITHMETIC_SIGNATURE
from .structure import fol_structure_to_hol_structure


if TYPE_CHECKING:
    from collections.abc import Callable

    from ....logic.structure.structure import FormalLogicStructure
    from ....rings.modular import Z3
    from ..structure import HolStructure


def test_fol_structure_to_hol_structure(fol_z3_model: FormalLogicStructure, hol_z3_model: HolStructure) -> None:
    translated_hol_model = fol_structure_to_hol_structure(fol_z3_model)

    assert translated_hol_model.sort_universes == {common.individual.value: fol_z3_model.universe}

    plus_sym = HOL_ARITHMETIC_SIGNATURE.get_nonlogical_constant_symbol('+')
    expected_interp = cast('Callable[[Z3], Callable[[Z3], Z3]]', hol_z3_model.interpretation[plus_sym])
    actual_interp = cast('Callable[[Z3], Callable[[Z3], Z3]]', translated_hol_model.interpretation[plus_sym])

    for a, b in itertools.product(fol_z3_model.universe, repeat=2):
        assert expected_interp(a)(b) == actual_interp(a)(b)
