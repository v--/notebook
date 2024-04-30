from .parsing import parse_rule
from .system import NaturalDeductionSystem


minimal_nd_system = NaturalDeductionSystem(
    frozenset([
        parse_rule('(∧⁺) φ, ψ ⫢ (φ ∧ ψ)'),
        parse_rule('(∧⁻ᴸ) (φ ∧ ψ) ⫢ φ'),
        parse_rule('(∧⁻ᴿ) (φ ∧ ψ) ⫢ ψ'),

        parse_rule('(∨⁺ᴸ) φ ⫢ (φ ∨ ψ)'),
        parse_rule('(∨⁺ᴿ) ψ ⫢ (φ ∨ ψ)'),
        parse_rule('(∨⁻) (φ ∨ ψ), [φ] θ, [ψ] θ ⫢ θ'),

        parse_rule('(→⁺) [φ] ψ ⫢ (φ → ψ)'),
        parse_rule('(→⁻) (φ → ψ), φ ⫢ ψ')
    ])
)
