from ..parsing import parse_signatureless_natural_deduction_rule
from .system import NaturalDeductionSystem


CLASSICAL_NATURAL_DEDUCTION_SYSTEM = NaturalDeductionSystem({
    '⊤₊':  parse_signatureless_natural_deduction_rule('⫢ ⊤'),
    '⊤₋':  parse_signatureless_natural_deduction_rule('[⊤] φ ⫢ φ'),

    'EFQ': parse_signatureless_natural_deduction_rule('⊥ ⫢ φ'),
    'DNE': parse_signatureless_natural_deduction_rule('[¬φ] ⊥ ⫢ φ'),

    '¬₊':  parse_signatureless_natural_deduction_rule('[φ] ⊥ ⫢ ¬φ'),
    '¬₋':  parse_signatureless_natural_deduction_rule('¬φ, φ ⫢ ⊥'),

    '∨₊ₗ': parse_signatureless_natural_deduction_rule('φ ⫢ (φ ∨ ψ)'),
    '∨₊ᵣ': parse_signatureless_natural_deduction_rule('ψ ⫢ (φ ∨ ψ)'),
    '∨₋':  parse_signatureless_natural_deduction_rule('(φ ∨ ψ), [φ] θ, [ψ] θ ⫢ θ'),

    '∧₊':  parse_signatureless_natural_deduction_rule('φ, ψ ⫢ (φ ∧ ψ)'),
    '∧₋ₗ': parse_signatureless_natural_deduction_rule('(φ ∧ ψ) ⫢ φ'),
    '∧₋ᵣ': parse_signatureless_natural_deduction_rule('(φ ∧ ψ) ⫢ ψ'),

    '→₊':  parse_signatureless_natural_deduction_rule('[φ] ψ ⫢ (φ → ψ)'),
    '→₋':  parse_signatureless_natural_deduction_rule('(φ → ψ), φ ⫢ ψ'),

    '↔₊':  parse_signatureless_natural_deduction_rule('[φ] ψ, [ψ] φ ⫢ (φ ↔ ψ)'),
    '↔₋ₗ': parse_signatureless_natural_deduction_rule('(φ ↔ ψ), φ ⫢ ψ'),
    '↔₋ᵣ': parse_signatureless_natural_deduction_rule('(φ ↔ ψ), ψ ⫢ φ'),
})
