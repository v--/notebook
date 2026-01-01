from ...parsing import parse_formula
from .signature import BOOLEAN_ALGEBRA_SIGNATURE


INEQUALITY_AXIOMS = [
    parse_formula('∀x.(x ≤ x)', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.∀y.∀z.(((x ≤ y) ∧ (y ≤ z)) → (x ≤ z))', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.∀y.(((x ≤ y) ∧ (y ≤ x)) → (x = y))', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.∀y.((x ≤ y) ↔ (y ≥ x))', BOOLEAN_ALGEBRA_SIGNATURE),
]


ASSOCIATIVITY_AXIOMS = [
    parse_formula('∀x.∀y.∀z.(((x ⩓ y) ⩓ z) = (x ⩓ (y ⩓ z)))', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.∀y.∀z.(((x ⩔ y) ⩔ z) = (x ⩔ (y ⩔ z)))', BOOLEAN_ALGEBRA_SIGNATURE),
]


COMMUTATIVITY_AXIOMS = [
    parse_formula('∀x.∀y.((x ⩓ y) = (y ⩓ x))', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.∀y.((x ⩔ y) = (y ⩔ x))', BOOLEAN_ALGEBRA_SIGNATURE),
]


ABSORPTION_AXIOMS = [
    parse_formula('∀x.∀y.((x ⩓ (x ⩔ y)) = x)', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.∀y.((x ⩔ (x ⩓ y)) = x)', BOOLEAN_ALGEBRA_SIGNATURE),
]


INEQUALITY_COMPATIBILITY_AXIOMS = [
    parse_formula('∀x.∀y.((x ≤ y) ↔ ((x ⩓ y) = x))', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.∀y.((x ≤ y) ↔ ((x ⩔ y) = y))', BOOLEAN_ALGEBRA_SIGNATURE),
]


EXTREMA_AXIOMS = [
    parse_formula('∀x.((x ⩓ ⫪) = x)', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.((x ⩔ ⫫) = x)', BOOLEAN_ALGEBRA_SIGNATURE),
]


COMPLEMENT_AXIOMS = [
    parse_formula('∀x.((x ⩔ ⫬x) = ⫪)', BOOLEAN_ALGEBRA_SIGNATURE),
    parse_formula('∀x.((x ⩓ ⫬x) = ⫫)', BOOLEAN_ALGEBRA_SIGNATURE),
]


BOOLEAN_ALGEBRA_AXIOMS = [
    *INEQUALITY_AXIOMS,
    *ASSOCIATIVITY_AXIOMS,
    *COMMUTATIVITY_AXIOMS,
    *ABSORPTION_AXIOMS,
    *INEQUALITY_COMPATIBILITY_AXIOMS,
    *EXTREMA_AXIOMS,
    *COMPLEMENT_AXIOMS
]
