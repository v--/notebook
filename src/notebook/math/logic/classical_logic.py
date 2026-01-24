from .deduction import NaturalDeductionSystem
from .parsing import parse_natural_deduction_rule


CLASSICAL_NATURAL_DEDUCTION_SYSTEM = NaturalDeductionSystem([
    parse_natural_deduction_rule('⊤₊', '⊩ ⊤'),

    parse_natural_deduction_rule('EFQ', '⊥ ⊩ φ'),
    parse_natural_deduction_rule('RAA', '[¬φ] ⊥ ⊩ φ'),

    parse_natural_deduction_rule('¬₊', '[φ] ⊥ ⊩ ¬φ'),
    parse_natural_deduction_rule('¬₋', '¬φ, φ ⊩ ⊥'),

    parse_natural_deduction_rule('∧₊', 'φ, ψ ⊩ (φ ∧ ψ)'),
    parse_natural_deduction_rule('∧₋ₗ', '(φ ∧ ψ) ⊩ φ'),
    parse_natural_deduction_rule('∧₋ᵣ', '(φ ∧ ψ) ⊩ ψ'),

    parse_natural_deduction_rule('∨₊ₗ', 'φ ⊩ [ψ] (φ ∨ ψ)'),
    parse_natural_deduction_rule('∨₊ᵣ', 'ψ ⊩ [φ] (φ ∨ ψ)'),
    parse_natural_deduction_rule('∨₋', '(φ ∨ ψ), [φ] θ, [ψ] θ ⊩ θ'),

    parse_natural_deduction_rule('→₊', '[φ] ψ ⊩ [φ] (φ → ψ)'),
    parse_natural_deduction_rule('→₋', '(φ → ψ), φ ⊩ ψ'),

    parse_natural_deduction_rule('↔₊', '[φ] ψ, [ψ] φ ⊩ (φ ↔ ψ)'),
    parse_natural_deduction_rule('↔₋ₗ', '(φ ↔ ψ), ψ ⊩ φ'),
    parse_natural_deduction_rule('↔₋ᵣ', '(φ ↔ ψ), φ ⊩ ψ'),

    parse_natural_deduction_rule('∀₊', 'φ[x ↦ y*] ⊩ ∀x.φ'),
    parse_natural_deduction_rule('∀₋', '∀x.φ ⊩ φ[x ↦ τ]'),

    parse_natural_deduction_rule('∃₊', 'φ[x ↦ τ] ⊩ ∃x.φ'),
    parse_natural_deduction_rule('∃₋', '∃x.φ, [φ[x ↦ y*]] ψ ⊩ ψ'),

    parse_natural_deduction_rule('=₊', '⊩ (τ = τ)'),
    parse_natural_deduction_rule('=₋', 'φ[x ↦ τ], (τ = σ) ⊩ φ[x ↦ σ]'),
])
