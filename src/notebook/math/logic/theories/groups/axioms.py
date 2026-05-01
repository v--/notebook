from ...parsing import parse_formula
from .signature import GROUP_SIGNATURE


GROUP_ASSOCIATIVITY = parse_formula('∀x.∀y.∀z.(((x ⋅ y) ⋅ z) = (x ⋅ (y ⋅ z)))', GROUP_SIGNATURE)
GROUP_NEUTRAL_LEFT = parse_formula('∀x.((x ⋅ 1) = x)', GROUP_SIGNATURE)
GROUP_NEUTRAL_RIGHT = parse_formula('∀x.((1 ⋅ x) = x)', GROUP_SIGNATURE)
GROUP_INVERSE_LEFT = parse_formula('∀x.((x ⋅ ~x) = 1)', GROUP_SIGNATURE)
GROUP_INVERSE_RIGHT = parse_formula('∀x.((x ⋅ ~x) = 1)', GROUP_SIGNATURE)
GROUP_AXIOMS = [GROUP_ASSOCIATIVITY, GROUP_NEUTRAL_LEFT, GROUP_NEUTRAL_RIGHT, GROUP_INVERSE_LEFT, GROUP_INVERSE_RIGHT]
GROUP_COMMUTATIVITY = parse_formula('∀x.∀y.((x ⋅ y) = (y ⋅ x))', GROUP_SIGNATURE)
