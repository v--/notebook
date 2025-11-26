from ..parsing import parse_formula
from .signature import GROUP_SIGNATURE


GROUP_ASSOCIATIVITY = parse_formula('∀x.∀y.∀z.(((x⋅y)⋅z) = (x⋅(y⋅z)))', GROUP_SIGNATURE)
GROUP_NEUTRAL_ELEMENT = parse_formula('∀x.(((x⋅1) = x) ∧ ((1⋅x) = x))', GROUP_SIGNATURE)
GROUP_INVERSE_ELEMENT = parse_formula('∀x.(((x⋅~(x)) = 1) ∧ ((~(x)⋅x) = 1))', GROUP_SIGNATURE)
GROUP_AXIOMS = [GROUP_ASSOCIATIVITY, GROUP_NEUTRAL_ELEMENT, GROUP_INVERSE_ELEMENT]
GROUP_COMMUTATIVITY = parse_formula('∀x.∀y.((x⋅y) = (y⋅x))', GROUP_SIGNATURE)
