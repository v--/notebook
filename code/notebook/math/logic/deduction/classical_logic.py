from ..parsing import parse_signatureless_natural_deduction_rule
from .system import NaturalDeductionSystem


classical_natural_deduction_system = NaturalDeductionSystem({
    '⊤⁺':  parse_signatureless_natural_deduction_rule('⫢ ⊤'),
    '⊤⁻':  parse_signatureless_natural_deduction_rule('[⊤] φ ⫢ φ'),

    'EFQ': parse_signatureless_natural_deduction_rule('⊥ ⫢ φ'),
    'DNE': parse_signatureless_natural_deduction_rule('[¬φ] ⊥ ⫢ φ'),

    '¬⁺':  parse_signatureless_natural_deduction_rule('[φ] ⊥ ⫢ ¬φ'),
    '¬⁻':  parse_signatureless_natural_deduction_rule('¬φ, φ ⫢ ⊥'),

    '∨⁺ᴸ': parse_signatureless_natural_deduction_rule('φ ⫢ (φ ∨ ψ)'),
    '∨⁺ᴿ': parse_signatureless_natural_deduction_rule('ψ ⫢ (φ ∨ ψ)'),
    '∨⁻':  parse_signatureless_natural_deduction_rule('(φ ∨ ψ), [φ] θ, [ψ] θ ⫢ θ'),

    '∧⁺':  parse_signatureless_natural_deduction_rule('φ, ψ ⫢ (φ ∧ ψ)'),
    '∧⁻ᴸ': parse_signatureless_natural_deduction_rule('(φ ∧ ψ) ⫢ φ'),
    '∧⁻ᴿ': parse_signatureless_natural_deduction_rule('(φ ∧ ψ) ⫢ ψ'),

    '→⁺':  parse_signatureless_natural_deduction_rule('[φ] ψ ⫢ (φ → ψ)'),
    '→⁻':  parse_signatureless_natural_deduction_rule('(φ → ψ), φ ⫢ ψ'),

    '↔⁺':  parse_signatureless_natural_deduction_rule('[φ] ψ, [ψ] φ ⫢ (φ ↔ ψ)'),
    '↔⁻ᴸ': parse_signatureless_natural_deduction_rule('(φ ↔ ψ), φ ⫢ ψ'),
    '↔⁻ᴿ': parse_signatureless_natural_deduction_rule('(φ ↔ ψ), ψ ⫢ φ'),
})
