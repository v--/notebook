from textwrap import dedent

from ....support.pytest import pytest_parametrize_kwargs
from ...logic.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...logic.deduction import proof_tree as ptree
from ...logic.instantiation import FormalLogicSchemaInstantiation
from ...logic.parsing import parse_formula, parse_formula_placeholder, parse_marker
from ...logic.signature import FormalLogicSignature
from ..algebraic_types import SIMPLE_ALGEBRAIC_SIGNATURE, SIMPLE_ALGEBRAIC_TYPE_SYSTEM
from ..instantiation import LambdaSchemaInstantiation
from ..parsing import (
    parse_type,
    parse_type_placeholder,
    parse_variable,
    parse_variable_assertion,
    parse_variable_placeholder,
)
from ..type_derivation import tree as dtree
from .derivation_to_proof import type_derivation_to_proof_tree, type_to_formula
from .proof_to_derivation import formula_to_type, proof_tree_to_type_derivation


@pytest_parametrize_kwargs(
    dict(type_='𝟘', formula='⊥'),
    dict(type_='𝟙', formula='⊤'),
    dict(type_='τ', formula='τ'),
    dict(type_='(τ → σ)', formula='(τ → σ)'),
    dict(type_='(τ × σ)', formula='(τ ∧ σ)'),
    dict(type_='(τ + σ)', formula='(τ ∨ σ)'),
    dict(type_='((𝟙 + 𝟘) × 𝟙)', formula='((⊤ ∨ ⊥) ∧ ⊤)'),
)
def test_type_to_formula(
    type_: str,
    formula: str,
    ch_logic_dummy_signature: FormalLogicSignature,
) -> None:
    parsed_type = parse_type(type_, SIMPLE_ALGEBRAIC_SIGNATURE)
    parsed_formula = parse_formula(formula, ch_logic_dummy_signature)
    assert type_to_formula(parsed_type) == parsed_formula
    assert formula_to_type(parsed_formula) == parsed_type


class TestTypeDerivationToProofTree:
    # x: τ
    def test_assumption(self, ch_logic_dummy_signature: FormalLogicSignature) -> None:
        derivation = dtree.assume(
            parse_variable_assertion('x: τ')
        )

        assert str(derivation) == dedent('''\
            x: τ
            '''
        )

        proof = ptree.assume(
            parse_formula('τ',ch_logic_dummy_signature),
            parse_marker('x')
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    # U₊: 𝟙
    def test_unit_intro(self) -> None:
        derivation = dtree.apply(SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟙₊'])
        proof = ptree.apply(CLASSICAL_NATURAL_DEDUCTION_SYSTEM['⊤₊'])

        assert str(derivation) == dedent('''\
            _____ 𝟙₊
            U₊: 𝟙
            '''
        )
        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    # The test here is mostly that instantiations are properly translated
    def test_empty_elim(self, ch_logic_dummy_signature: FormalLogicSignature) -> None:
        derivation = dtree.apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟘₋'],
            dtree.assume(
                parse_variable_assertion('x: 𝟘', SIMPLE_ALGEBRAIC_SIGNATURE),
            ),
            instantiation=LambdaSchemaInstantiation(
                type_mapping={
                    parse_type_placeholder('τ'): parse_type('τ')
                }
            )
        )

        assert str(derivation) == dedent('''\
             x: 𝟘
            ________ 𝟘₋
            (E₋x): τ
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['EFQ'],
            ptree.assume(
                parse_formula('⊥', ch_logic_dummy_signature),
                parse_marker('x')
            ),
            instantiation=FormalLogicSchemaInstantiation(
                formula_mapping={
                    parse_formula_placeholder('φ'): parse_formula('τ', ch_logic_dummy_signature)
                }
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    def test_arrow_intro(self, ch_logic_dummy_signature: FormalLogicSignature) -> None:
        derivation = dtree.apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₊'],
            dtree.premise(
                discharge=parse_variable_assertion('x: τ'),
                tree=dtree.assume(
                    parse_variable_assertion('y: σ')
                )
            )
        )

        assert str(derivation) == dedent('''\
                 y: σ
            _________________ →₊
            (λx:τ.y): (τ → σ)
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
            ptree.premise(
                discharge=parse_formula('τ', ch_logic_dummy_signature),
                marker=parse_marker('x'),
                tree=ptree.assume(
                    parse_formula('σ', ch_logic_dummy_signature),
                    parse_marker('y')
                )
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    def test_prod_intro(self, ch_logic_dummy_signature: FormalLogicSignature) -> None:
        derivation = dtree.apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×₊'],
            dtree.assume(
                parse_variable_assertion('x: τ')
            ),
            dtree.assume(
                parse_variable_assertion('y: σ')
            )
        )

        assert str(derivation) == dedent('''\
            x: τ      y: σ
            _________________ ×₊
            ((P₊x)y): (τ × σ)
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧₊'],
            ptree.assume(
                parse_formula('τ', ch_logic_dummy_signature),
                parse_marker('x')
            ),
            ptree.assume(
                parse_formula('σ', ch_logic_dummy_signature),
                parse_marker('y')
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    def test_prod(self, ch_logic_dummy_signature: FormalLogicSignature) -> None:
        derivation = dtree.apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×₋ₗ'],
            dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×₊'],
                dtree.assume(
                    parse_variable_assertion('x: τ')
                ),
                dtree.assume(
                    parse_variable_assertion('y: σ')
                )
            )
        )

        assert str(derivation) == dedent('''\
            x: τ      y: σ
            _________________ ×₊
            ((P₊x)y): (τ × σ)
            _________________ ×₋ₗ
            (P₋ₗ((P₊x)y)): τ
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧₋ₗ'],
            ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧₊'],
                ptree.assume(
                    parse_formula('τ', ch_logic_dummy_signature),
                    parse_marker('x')
                ),
                ptree.assume(
                    parse_formula('σ', ch_logic_dummy_signature),
                    parse_marker('y')
                )
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    # This can be found in the proof that τ ⧦ τ + 𝟘 in thm:simple_algebraic_type_arithmetic
    def test_sum(self, ch_logic_dummy_signature: FormalLogicSignature) -> None:
        derivation = dtree.apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₋'],
            dtree.assume(
                parse_variable_assertion('x: (τ + 𝟘)', SIMPLE_ALGEBRAIC_SIGNATURE)
            ),
            dtree.premise(
                tree=dtree.assume(
                    parse_variable_assertion('a: τ')
                ),
                discharge=parse_variable_assertion('a: τ')
            ),
            dtree.premise(
                tree=dtree.apply(
                    SIMPLE_ALGEBRAIC_TYPE_SYSTEM['𝟘₋'],
                    dtree.assume(
                        parse_variable_assertion('b: 𝟘', SIMPLE_ALGEBRAIC_SIGNATURE),
                    ),
                    instantiation=LambdaSchemaInstantiation(
                        type_mapping={
                            parse_type_placeholder('τ'): parse_type('τ')
                        }
                    )
                ),
                discharge=parse_variable_assertion('b: 𝟘', SIMPLE_ALGEBRAIC_SIGNATURE)
            )
        )

        assert str(derivation) == dedent('''\
                                            b: 𝟘
                                           ________ 𝟘₋
                 x: (τ + 𝟘)      a: τ      (E₋b): τ
            a, b __________________________________ +₋
                  (((S₋(λa:τ.a))(λb:𝟘.(E₋b)))x): τ
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₋'],
            ptree.assume(
                parse_formula('(τ ∨ ⊥)', ch_logic_dummy_signature),
                parse_marker('x')
            ),
            ptree.premise(
                tree=ptree.assume(
                    parse_formula('τ', ch_logic_dummy_signature),
                    parse_marker('a')
                ),
                discharge=parse_formula('τ', ch_logic_dummy_signature),
                marker=parse_marker('a')
            ),
            ptree.premise(
                tree=ptree.apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['EFQ'],
                    ptree.assume(
                        parse_formula('⊥', ch_logic_dummy_signature),
                        parse_marker('b')
                    ),
                    instantiation=FormalLogicSchemaInstantiation(
                        formula_mapping={
                            parse_formula_placeholder('φ'): parse_formula('τ', ch_logic_dummy_signature)
                        }
                    )
                ),
                discharge=parse_formula('⊥', ch_logic_dummy_signature),
                marker=parse_marker('b')
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    def test_unused_discharged_assertions(self, ch_logic_dummy_signature: FormalLogicSignature) -> None:
        derivation = dtree.apply(
            SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₋'],
            dtree.apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×₋ᵣ'],
                dtree.assume(
                    parse_variable_assertion('x: (τ × (σ + ρ))'),
                )
            ),
            dtree.premise(
                tree=dtree.apply(
                    SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ᵣ'],
                    dtree.assume(
                        parse_variable_assertion('a: σ'),
                    ),
                    instantiation=LambdaSchemaInstantiation(
                        type_mapping={
                            parse_type_placeholder('τ'): parse_type('τ')
                        }
                    )
                ),
                discharge=parse_variable_assertion('a: σ')
            ),
            dtree.premise(
                tree=dtree.apply(
                    SIMPLE_ALGEBRAIC_TYPE_SYSTEM['+₊ₗ'],
                    dtree.apply(
                        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['×₋ₗ'],
                        dtree.assume(
                            parse_variable_assertion('x: (τ × (σ + ρ))'),
                        )
                    ),
                    instantiation=LambdaSchemaInstantiation(
                        type_mapping={
                            parse_type_placeholder('σ'): parse_type('σ')
                        }
                    )
                ),
                discharge=parse_variable_assertion('b: ρ')
            ),
            instantiation=LambdaSchemaInstantiation(
                variable_mapping={
                    parse_variable_placeholder('y'): parse_variable('b'),
                }
            )
        )

        assert str(derivation) == dedent('''\
                                                                x: (τ × (σ + ρ))
                                                                __________________ ×₋ₗ
              x: (τ × (σ + ρ))              a: σ                    (P₋ₗx): τ
              __________________ ×₋ᵣ    _______________ +₊ᵣ    ____________________ +₊ₗ
               (P₋ᵣx): (σ + ρ)          (S₊ᵣa): (τ + σ)        (S₊ₗ(P₋ₗx)): (τ + σ)
            a _____________________________________________________________________ +₋
                     (((S₋(λa:σ.(S₊ᵣa)))(λb:ρ.(S₊ₗ(P₋ₗx))))(P₋ᵣx)): (τ + σ)
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₋'],
            ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧₋ᵣ'],
                ptree.assume(
                    parse_formula('(τ ∧ (σ ∨ ρ))', ch_logic_dummy_signature),
                    marker=parse_marker('x')
                )
            ),
            ptree.premise(
                tree=ptree.apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ᵣ'],
                    ptree.assume(
                        parse_formula('σ', ch_logic_dummy_signature),
                        marker=parse_marker('a')
                    ),
                    instantiation=FormalLogicSchemaInstantiation(
                        formula_mapping={
                            parse_formula_placeholder('φ'): parse_formula('τ', ch_logic_dummy_signature)
                        }
                    )
                ),
                marker=parse_marker('a'),
                discharge=parse_formula('σ', ch_logic_dummy_signature)
            ),
            ptree.premise(
                tree=ptree.apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ₗ'],
                    ptree.apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧₋ₗ'],
                        ptree.assume(
                            parse_formula('(τ ∧ (σ ∨ ρ))', ch_logic_dummy_signature),
                            marker=parse_marker('x')
                        )
                    ),
                    instantiation=FormalLogicSchemaInstantiation(
                        formula_mapping={
                            parse_formula_placeholder('ψ'): parse_formula('σ', ch_logic_dummy_signature)
                        }
                    )
                ),
                marker=parse_marker('b'),
                discharge=parse_formula('ρ', ch_logic_dummy_signature)
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation
