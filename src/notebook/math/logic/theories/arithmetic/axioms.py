from typing import TYPE_CHECKING

from ...instantiation import AtomicLogicSchemaInstantiation, instantiate_formula_schema
from ...parsing import (
    parse_formula,
    parse_formula_placeholder,
    parse_formula_schema,
    parse_variable,
    parse_variable_placeholder,
)
from ...transformation import universal_closure
from .signature import ARITHMETIC_SIGNATURE


if TYPE_CHECKING:
    from ...formulas import Formula
    from ...terms import Variable


PEANO_NO_ZERO_PREDECESSOR = parse_formula('¬∃x.(Sx = 0)', ARITHMETIC_SIGNATURE)
PEANO_INJECTIVITY = universal_closure(parse_formula('((Sx = Sy) → (x = y))', ARITHMETIC_SIGNATURE))
PEANO_INDUCTION_SCHEMA = parse_formula_schema(
    '((φ[x ↦ 0] ∧ ∀n.(φ[x ↦ n] → φ[x ↦ Sn])) → ∀n.φ[x ↦ n])',
    ARITHMETIC_SIGNATURE,
)


def get_induction_axiom(formula: Formula, var_x: Variable | None = None, var_n: Variable | None = None) -> Formula:
    instantiation = AtomicLogicSchemaInstantiation(
        formula_mapping={parse_formula_placeholder('φ'): formula},
        variable_mapping={
            parse_variable_placeholder('x'): var_x or parse_variable('x'),
            parse_variable_placeholder('n'): var_n or parse_variable('n'),
        },
    )

    return instantiate_formula_schema(PEANO_INDUCTION_SCHEMA, instantiation)


PEANO_ADDITION_AXIOMS = [
    universal_closure(parse_formula('((x + 0) = x)', ARITHMETIC_SIGNATURE)),
    universal_closure(parse_formula('((x + Sy) = S(x + y))', ARITHMETIC_SIGNATURE)),
]

PEANO_MULTIPLICATION_AXIOMS = [
    universal_closure(parse_formula('((x × 0) = 0)', ARITHMETIC_SIGNATURE)),
    universal_closure(parse_formula('((x × Sy) = ((x × y) + x))', ARITHMETIC_SIGNATURE)),
]
