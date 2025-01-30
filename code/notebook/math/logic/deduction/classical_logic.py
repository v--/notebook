from ..parsing import parse_signatureless_natural_deduction_rule
from .rules import NaturalDeductionSystem


classical_natural_deduction_system = NaturalDeductionSystem([
    parse_signatureless_natural_deduction_rule('(⊤⁺) ⫢ ⊤'),
    parse_signatureless_natural_deduction_rule('(⊤⁻) [⊤] φ ⫢ φ'),

    parse_signatureless_natural_deduction_rule('(EFQ) ⊥ ⫢ φ'),
    parse_signatureless_natural_deduction_rule('(DNE) [¬φ] ⊥ ⫢ φ'),

    parse_signatureless_natural_deduction_rule('(¬⁺) [φ] ⊥ ⫢ ¬φ'),
    parse_signatureless_natural_deduction_rule('(¬⁻) ¬φ, φ ⫢ ⊥'),

    parse_signatureless_natural_deduction_rule('(∨⁺ᴸ) φ ⫢ (φ ∨ ψ)'),
    parse_signatureless_natural_deduction_rule('(∨⁺ᴿ) ψ ⫢ (φ ∨ ψ)'),
    parse_signatureless_natural_deduction_rule('(∨⁻) (φ ∨ ψ), [φ] θ, [ψ] θ ⫢ θ'),

    parse_signatureless_natural_deduction_rule('(∧⁺) φ, ψ ⫢ (φ ∧ ψ)'),
    parse_signatureless_natural_deduction_rule('(∧⁻ᴸ) (φ ∧ ψ) ⫢ φ'),
    parse_signatureless_natural_deduction_rule('(∧⁻ᴿ) (φ ∧ ψ) ⫢ ψ'),

    parse_signatureless_natural_deduction_rule('(→⁺) [φ] ψ ⫢ (φ → ψ)'),
    parse_signatureless_natural_deduction_rule('(→⁻) (φ → ψ), φ ⫢ ψ'),

    parse_signatureless_natural_deduction_rule('(↔⁺) [φ] ψ, [ψ] φ ⫢ (φ ↔ ψ)'),
    parse_signatureless_natural_deduction_rule('(↔⁻ᴸ) (φ ↔ ψ), φ ⫢ ψ'),
    parse_signatureless_natural_deduction_rule('(↔⁻ᴿ) (φ ↔ ψ), ψ ⫢ φ')
])
