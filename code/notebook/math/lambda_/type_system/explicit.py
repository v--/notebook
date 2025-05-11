from collections.abc import Mapping

from ..parsing import parse_typing_rule
from ..signature import EMPTY_SIGNATURE, LambdaSignature
from ..typing import ExplicitTypingRule, TypingStyle
from .gradual import GradualTypeSystem


class ExplicitTypeSystem(GradualTypeSystem[ExplicitTypingRule]):
    rules: Mapping[str, ExplicitTypingRule]


BASE_EXPLICIT_TYPE_SYSTEM = ExplicitTypeSystem({
    '→₊': parse_typing_rule(EMPTY_SIGNATURE, '[x: τ] M: σ ⫢ (λx:τ.M): (τ → σ)', TypingStyle.EXPLICIT),
    '→₋': parse_typing_rule(EMPTY_SIGNATURE, 'M: (τ → σ), N: τ ⫢ (MN): σ', TypingStyle.EXPLICIT)
})


SIMPLE_SIGNATURE = LambdaSignature(
    base_types=['0', '1'],
    constant_terms=['E₋', 'U₊', 'P₊', 'P₋ₗ', 'P₋ᵣ', 'S₊ₗ', 'S₊ᵣ', 'S₋']
)


SIMPLE_ALGEBRAIC_TYPE_SYSTEM = ExplicitTypeSystem({
    **BASE_EXPLICIT_TYPE_SYSTEM.rules,
    '0₋': parse_typing_rule(SIMPLE_SIGNATURE, 'M: 0 ⫢ (E₋M): τ', TypingStyle.EXPLICIT),
    '1₊': parse_typing_rule(SIMPLE_SIGNATURE, '⫢ U₊: 1', TypingStyle.EXPLICIT),
    '1₋': parse_typing_rule(SIMPLE_SIGNATURE, '[U₊: 1] M: τ ⫢ M: τ', TypingStyle.EXPLICIT),
    '×₊': parse_typing_rule(SIMPLE_SIGNATURE, 'M: τ, N: σ ⫢ ((P₊M)N): (τ × σ)', TypingStyle.EXPLICIT),
    '×₋ₗ': parse_typing_rule(SIMPLE_SIGNATURE, 'K: (τ × σ) ⫢ (P₋ₗK): τ', TypingStyle.EXPLICIT),
    '×₋ᵣ': parse_typing_rule(SIMPLE_SIGNATURE, 'K: (τ × σ) ⫢ (P₋ᵣK): σ', TypingStyle.EXPLICIT),
    '+₊ₗ': parse_typing_rule(SIMPLE_SIGNATURE, 'M: τ ⫢ (S₊ₗM): (τ + σ)', TypingStyle.EXPLICIT),
    '+₊ᵣ': parse_typing_rule(SIMPLE_SIGNATURE, 'N: σ ⫢ (S₊ᵣN): (τ + σ)', TypingStyle.EXPLICIT),
    '+₋': parse_typing_rule(SIMPLE_SIGNATURE, 'M: (τ + σ), [x: τ] N: ρ, [y: σ] K: ρ ⫢ (((S₋(λx:τ.N))(λy:σ.K))M): ρ', TypingStyle.EXPLICIT),
})
