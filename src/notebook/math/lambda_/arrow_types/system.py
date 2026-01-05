from ..parsing import parse_typing_rule
from ..type_system import ExplicitTypeSystem


ARROW_ONLY_TYPE_SYSTEM = ExplicitTypeSystem([
    parse_typing_rule('→₊', '[x: τ] M: σ ⊩ (λx:τ.M): (τ → σ)'),
    parse_typing_rule('→₋', 'M: (τ → σ), N: τ ⊩ (MN): σ')
])
