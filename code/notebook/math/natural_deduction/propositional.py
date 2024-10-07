from ..fol.formulas import Formula
from ..fol.parsing import parse_propositional_formula
from .parsing import parse_rule
from .proof_tree import AssumptionTree, ProofTree, RuleApplicationTree, apply, assume
from .substitution import substitute
from .system import NaturalDeductionSystem


def substitute_propositional_formulas(schema: str, **kwargs: str) -> Formula:
    return substitute(
        schema,
        **{key: parse_propositional_formula(value) for key, value in kwargs.items()}
    )


propositional_natural_deduction_system = NaturalDeductionSystem([
    parse_rule('(⊤⁺) ⫢ ⊤'),
    parse_rule('(⊤⁻) [⊤] φ ⫢ φ'),

    parse_rule('(EFQ) ⊥ ⫢ φ'),
    parse_rule('(DNE) [¬φ] ⊥ ⫢ φ'),

    parse_rule('(¬⁺) [φ] ⊥ ⫢ ¬φ'),
    parse_rule('(¬⁻) ¬φ, φ ⫢ ⊥'),

    parse_rule('(∨⁺ᴸ) φ ⫢ (φ ∨ ψ)'),
    parse_rule('(∨⁺ᴿ) ψ ⫢ (φ ∨ ψ)'),
    parse_rule('(∨⁻) (φ ∨ ψ), [φ] θ, [ψ] θ ⫢ θ'),

    parse_rule('(∧⁺) φ, ψ ⫢ (φ ∧ ψ)'),
    parse_rule('(∧⁻ᴸ) (φ ∧ ψ) ⫢ φ'),
    parse_rule('(∧⁻ᴿ) (φ ∧ ψ) ⫢ ψ'),

    parse_rule('(→⁺) [φ] ψ ⫢ (φ → ψ)'),
    parse_rule('(→⁻) (φ → ψ), φ ⫢ ψ'),

    parse_rule('(↔⁺) [φ] ψ, [ψ] φ ⫢ (φ ↔ ψ)'),
    parse_rule('(↔⁻ᴸ) (φ ↔ ψ), φ ⫢ ψ'),
    parse_rule('(↔⁻ᴿ) (φ ↔ ψ), ψ ⫢ φ')
])


def propositional_assume(formula: Formula | str, marker: str) -> AssumptionTree:
    return assume(
        propositional_natural_deduction_system,
        parse_propositional_formula(formula) if isinstance(formula, str) else formula,
        marker
    )


def propositional_apply(rule_name: str, *args: ProofTree, **kwargs: Formula | str) -> RuleApplicationTree:
    parsed_kwargs = {
        key: parse_propositional_formula(value) if isinstance(value, str) else value
        for key, value in kwargs.items()
    }

    return apply(
        propositional_natural_deduction_system,
        rule_name,
        *args,
        **parsed_kwargs
    )
