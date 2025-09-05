from ..arrow_types import ARROW_ONLY_TYPE_SYSTEM
from ..parsing import parse_typing_rule
from ..signature import LambdaSignature
from ..type_system import ExplicitTypeSystem


SIMPLE_ALGEBRAIC_SIGNATURE = LambdaSignature(
    base_types=['0', '1'],
    constant_terms=['E₋', 'U₊', 'P₊', 'P₋ₗ', 'P₋ᵣ', 'S₊ₗ', 'S₊ᵣ', 'S₋']
)


SIMPLE_ALGEBRAIC_TYPE_SYSTEM = ExplicitTypeSystem([
    *ARROW_ONLY_TYPE_SYSTEM.rules,

    parse_typing_rule('0₋', 'M: 0 ⫢ (E₋M): τ', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('1₊', '⫢ U₊: 1', SIMPLE_ALGEBRAIC_SIGNATURE),

    parse_typing_rule('×₊', 'M: τ, N: σ ⫢ ((P₊M)N): (τ × σ)', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('×₋ₗ', 'K: (τ × σ) ⫢ (P₋ₗK): τ', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('×₋ᵣ', 'K: (τ × σ) ⫢ (P₋ᵣK): σ', SIMPLE_ALGEBRAIC_SIGNATURE),

    parse_typing_rule('+₊ₗ', 'M: τ ⫢ (S₊ₗM): (τ + σ)', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('+₊ᵣ', 'N: σ ⫢ (S₊ᵣN): (τ + σ)', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('+₋', 'M: (τ + σ), [x: τ] N: ρ, [y: σ] K: ρ ⫢ (((S₋(λx:τ.N))(λy:σ.K))M): ρ', SIMPLE_ALGEBRAIC_SIGNATURE),
])
