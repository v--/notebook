from textwrap import dedent

from ....support.pytest import pytest_parametrize_kwargs
from ...logic.deduction import proof_tree as ptree
from ...logic.deduction.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...logic.instantiation import FormalLogicSchemaInstantiation
from ...logic.parsing import parse_formula, parse_formula_placeholder, parse_marker
from ...logic.signature import FormalLogicSignature
from ..instantiation import LambdaSchemaInstantiation
from ..parsing import (
    parse_type,
    parse_type_placeholder,
    parse_variable_assertion,
)
from ..signature import LambdaSignature
from ..type_derivation import tree as dtree
from ..type_system import EXPLICIT_SIMPLE_TYPE_SYSTEM
from .derivation_to_proof import type_derivation_to_proof_tree, type_to_formula
from .proof_to_derivation import formula_to_type, proof_tree_to_type_derivation


@pytest_parametrize_kwargs(
    dict(type_='0', formula='⊥'),
    dict(type_='1', formula='⊤'),
    dict(type_='τ', formula='τ'),
    dict(type_='(τ → σ)', formula='(τ → σ)'),
    dict(type_='(τ × σ)', formula='(τ ∧ σ)'),
    dict(type_='(τ + σ)', formula='(τ ∨ σ)'),
    dict(type_='((1 + 0) × 1)', formula='((⊤ ∨ ⊥) ∧ ⊤)'),
)
def test_type_to_formula(
    type_: str,
    formula: str,
    ch_logic_dummy_signature: FormalLogicSignature,
    ch_lambda_dummy_signature: LambdaSignature
) -> None:
    parsed_type = parse_type(ch_lambda_dummy_signature, type_)
    parsed_formula = parse_formula(ch_logic_dummy_signature, formula)
    assert type_to_formula(parsed_type) == parsed_formula
    assert formula_to_type(parsed_formula) == parsed_type


class TestTypeDerivationToProofTree:
    # x: τ
    def test_assumption(
        self,
        ch_logic_dummy_signature: FormalLogicSignature,
        ch_lambda_dummy_signature: LambdaSignature
    ) -> None:
        derivation = dtree.assume(
            parse_variable_assertion(ch_lambda_dummy_signature, 'x: τ')
        )

        assert str(derivation) == dedent('''\
            x: τ
            '''
        )

        proof = ptree.assume(
            parse_formula(ch_logic_dummy_signature, 'τ'),
            parse_marker('x')
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    # U₊: 1
    def test_unit_intro(self) -> None:
        derivation = dtree.apply(EXPLICIT_SIMPLE_TYPE_SYSTEM, '1₊')
        proof = ptree.apply(CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '⊤₊')

        assert str(derivation) == dedent('''\
            _____ 1₊
            U₊: 1
            '''
        )
        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    # The test here is mostly that instantiations are properly translated
    def test_empty_elim(
        self,
        ch_logic_dummy_signature: FormalLogicSignature,
        ch_lambda_dummy_signature: LambdaSignature
    ) -> None:
        derivation = dtree.apply(
            EXPLICIT_SIMPLE_TYPE_SYSTEM, '0₋',
            dtree.assume(
                parse_variable_assertion(ch_lambda_dummy_signature, 'x: 0'),
            ),
            instantiation=LambdaSchemaInstantiation(
                type_mapping={
                    parse_type_placeholder('τ'): parse_type(ch_lambda_dummy_signature, 'τ')
                }
            )
        )

        assert str(derivation) == dedent('''\
             x: 0
            ________ 0₋
            (E₋x): τ
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM, 'EFQ',
            ptree.assume(
                parse_formula(ch_logic_dummy_signature, '⊥'),
                parse_marker('x')
            ),
            instantiation=FormalLogicSchemaInstantiation(
                formula_mapping={
                    parse_formula_placeholder('φ'): parse_formula(ch_logic_dummy_signature, 'τ')
                }
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    def test_arrow_intro(
        self,
        ch_logic_dummy_signature: FormalLogicSignature,
        ch_lambda_dummy_signature: LambdaSignature
    ) -> None:
        derivation = dtree.apply(
            EXPLICIT_SIMPLE_TYPE_SYSTEM, '→₊',
            dtree.premise(
                discharge=parse_variable_assertion(ch_lambda_dummy_signature, 'x: τ'),
                tree=dtree.assume(
                    parse_variable_assertion(ch_lambda_dummy_signature, 'y: σ')
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
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '→₊',
            ptree.premise(
                discharge=parse_formula(ch_logic_dummy_signature, 'τ'),
                marker=parse_marker('x'),
                tree=ptree.assume(
                    parse_formula(ch_logic_dummy_signature, 'σ'),
                    parse_marker('y')
                )
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    def test_prod_intro(
        self,
        ch_logic_dummy_signature: FormalLogicSignature,
        ch_lambda_dummy_signature: LambdaSignature
    ) -> None:
        derivation = dtree.apply(
            EXPLICIT_SIMPLE_TYPE_SYSTEM, '×₊',
            dtree.assume(
                parse_variable_assertion(ch_lambda_dummy_signature, 'x: τ')
            ),
            dtree.assume(
                parse_variable_assertion(ch_lambda_dummy_signature, 'y: σ')
            )
        )

        assert str(derivation) == dedent('''\
            x: τ      y: σ
            _________________ ×₊
            ((P₊x)y): (τ × σ)
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '∧₊',
            ptree.assume(
                parse_formula(ch_logic_dummy_signature, 'τ'),
                parse_marker('x')
            ),
            ptree.assume(
                parse_formula(ch_logic_dummy_signature, 'σ'),
                parse_marker('y')
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    def test_prod(
        self,
        ch_logic_dummy_signature: FormalLogicSignature,
        ch_lambda_dummy_signature: LambdaSignature
    ) -> None:
        derivation = dtree.apply(
            EXPLICIT_SIMPLE_TYPE_SYSTEM, '×₋ₗ',
            dtree.apply(
                EXPLICIT_SIMPLE_TYPE_SYSTEM, '×₊',
                dtree.assume(
                    parse_variable_assertion(ch_lambda_dummy_signature, 'x: τ')
                ),
                dtree.assume(
                    parse_variable_assertion(ch_lambda_dummy_signature, 'y: σ')
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
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '∧₋ₗ',
            ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '∧₊',
                ptree.assume(
                    parse_formula(ch_logic_dummy_signature, 'τ'),
                    parse_marker('x')
                ),
                ptree.assume(
                    parse_formula(ch_logic_dummy_signature, 'σ'),
                    parse_marker('y')
                )
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation

    def test_sum(
        self,
        ch_logic_dummy_signature: FormalLogicSignature,
        ch_lambda_dummy_signature: LambdaSignature
    ) -> None:
        derivation = dtree.apply(
            EXPLICIT_SIMPLE_TYPE_SYSTEM, '+₋',
            dtree.apply(
                EXPLICIT_SIMPLE_TYPE_SYSTEM, '+₊ₗ',
                dtree.assume(
                    parse_variable_assertion(ch_lambda_dummy_signature, 'x: τ')
                ),
                instantiation=LambdaSchemaInstantiation(
                    type_mapping={
                        parse_type_placeholder('σ'): parse_type(ch_lambda_dummy_signature, '0')
                    }
                )
            ),
            dtree.premise(
                tree=dtree.assume(
                    parse_variable_assertion(ch_lambda_dummy_signature, 'x: τ')
                ),
                discharge=parse_variable_assertion(ch_lambda_dummy_signature, 'x: τ')
            ),
            dtree.premise(
                tree=dtree.apply(
                    EXPLICIT_SIMPLE_TYPE_SYSTEM, '0₋',
                    dtree.assume(
                        parse_variable_assertion(ch_lambda_dummy_signature, 'y: 0'),
                    ),
                    instantiation=LambdaSchemaInstantiation(
                        type_mapping={
                            parse_type_placeholder('τ'): parse_type(ch_lambda_dummy_signature, 'τ')
                        }
                    )
                ),
                discharge=parse_variable_assertion(ch_lambda_dummy_signature, 'y: 0')
            )
        )

        assert str(derivation) == dedent('''\
                     x: τ                          y: 0
                 _______________ +₊ₗ              ________ 0₋
                 (S₊ₗx): (τ + 0)        x: τ      (E₋y): τ
            x _______________________________________________ +₋
              (((S₋(S₊ₗ(λx:τ.x)))(S₊ᵣ(λx:0.(E₋y))))(S₊ₗx)): τ
            '''
        )

        proof = ptree.apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '∨₋',
            ptree.apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM, '∨₊ₗ',
                ptree.assume(
                    parse_formula(ch_logic_dummy_signature, 'τ'),
                    parse_marker('x')
                ),
                instantiation=FormalLogicSchemaInstantiation(
                    formula_mapping={
                        parse_formula_placeholder('ψ'): parse_formula(ch_logic_dummy_signature, '⊥')
                    }
                )
            ),
            ptree.premise(
                tree=ptree.assume(
                    parse_formula(ch_logic_dummy_signature, 'τ'),
                    parse_marker('x')
                ),
                discharge=parse_formula(ch_logic_dummy_signature, 'τ'),
                marker=parse_marker('x')
            ),
            ptree.premise(
                tree=ptree.apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM, 'EFQ',
                    ptree.assume(
                        parse_formula(ch_logic_dummy_signature, '⊥'),
                        parse_marker('y')
                    ),
                    instantiation=FormalLogicSchemaInstantiation(
                        formula_mapping={
                            parse_formula_placeholder('φ'): parse_formula(ch_logic_dummy_signature, 'τ')
                        }
                    )
                ),
                discharge=parse_formula(ch_logic_dummy_signature, '⊥'),
                marker=parse_marker('y')
            )
        )

        assert type_derivation_to_proof_tree(derivation) == proof
        assert proof_tree_to_type_derivation(proof) == derivation
