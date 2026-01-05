from ..arrow_types import ARROW_ONLY_TYPE_SYSTEM
from ..parsing import parse_typing_rule
from ..signature import BaseTypeSymbol, ConstantTermSymbol, LambdaSignature
from ..type_system import ExplicitTypeSystem


SIMPLE_ALGEBRAIC_SIGNATURE = LambdaSignature(
    BaseTypeSymbol('𝟘'),
    BaseTypeSymbol('𝟙'),
    ConstantTermSymbol('E₋'),
    ConstantTermSymbol('U₊'),
    ConstantTermSymbol('P₊'),
    ConstantTermSymbol('P₋ₗ'),
    ConstantTermSymbol('P₋ᵣ'),
    ConstantTermSymbol('S₊ₗ'),
    ConstantTermSymbol('S₊ᵣ'),
    ConstantTermSymbol('S₋')
)


SIMPLE_ALGEBRAIC_TYPE_SYSTEM = ExplicitTypeSystem([
    *ARROW_ONLY_TYPE_SYSTEM.rules,

    parse_typing_rule('𝟘₋', 'M: 𝟘 ⊩ (E₋M): τ', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('𝟙₊', '⊩ U₊: 𝟙', SIMPLE_ALGEBRAIC_SIGNATURE),

    parse_typing_rule('×₊', 'M: τ, N: σ ⊩ ((P₊M)N): (τ × σ)', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('×₋ₗ', 'K: (τ × σ) ⊩ (P₋ₗK): τ', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('×₋ᵣ', 'K: (τ × σ) ⊩ (P₋ᵣK): σ', SIMPLE_ALGEBRAIC_SIGNATURE),

    parse_typing_rule('+₊ₗ', 'M: τ ⊩ (S₊ₗM): (τ + σ)', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('+₊ᵣ', 'N: σ ⊩ (S₊ᵣN): (τ + σ)', SIMPLE_ALGEBRAIC_SIGNATURE),
    parse_typing_rule('+₋', 'M: (τ + σ), [x: τ] N: ρ, [y: σ] K: ρ ⊩ (((S₋(λx:τ.N))(λy:σ.K))M): ρ', SIMPLE_ALGEBRAIC_SIGNATURE),
])
