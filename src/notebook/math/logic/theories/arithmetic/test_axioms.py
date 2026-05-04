from textwrap import dedent

from notebook.math.logic.classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from notebook.math.logic.deduction.proof_tree import apply, premise_config
from notebook.math.logic.formulas import ConnectiveFormula, QuantifierFormula
from notebook.math.logic.instantiation import AtomicLogicSchemaInstantiation
from notebook.math.logic.parsing import (
    parse_formula,
    parse_formula_placeholder,
    parse_formula_with_substitution,
    parse_term,
    parse_term_placeholder,
    parse_variable,
)
from notebook.math.logic.substitution import substitute_in_formula
from notebook.support.coderefs import collector

from .axioms import get_induction_axiom
from .signature import ARITHMETIC_SIGNATURE


def test_induction_instance() -> None:
    axiom = get_induction_axiom(parse_formula('(x ≤ Sx)', ARITHMETIC_SIGNATURE))
    expected = parse_formula('(((0 ≤ S0) ∧ ∀n.((n ≤ Sn) → (Sn ≤ SSn))) → ∀n.(n ≤ Sn))', ARITHMETIC_SIGNATURE)
    assert axiom == expected


@collector.ref('thm:peano_arithmetic_predecessor_existence')
def test_predecessor_existence_proof() -> None:
    target = parse_formula('∀x.((x = 0) ∨ ∃y.(x = Sy))', ARITHMETIC_SIGNATURE)
    assert isinstance(target, QuantifierFormula)

    aux = target.body
    induction_axiom = get_induction_axiom(aux)
    assert isinstance(induction_axiom, ConnectiveFormula)

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧₊'],
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ₗ'],
            apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['=₊'],
                instantiation=AtomicLogicSchemaInstantiation(
                    term_mapping={
                        parse_term_placeholder('τ'): parse_term('0', ARITHMETIC_SIGNATURE),
                    },
                ),
            ),
            instantiation=AtomicLogicSchemaInstantiation(
                formula_mapping={
                    parse_formula_placeholder('ψ'): parse_formula('∃y.(0 = Sy)', ARITHMETIC_SIGNATURE),
                },
            ),
        ),
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
            premise_config(
                main=parse_formula_with_substitution('(((n = 0) ∨ ∃y.(n = Sy)) → ((Sn = 0) ∨ ∃y.(Sn = Sy)))[n ↦ n]', ARITHMETIC_SIGNATURE),
                tree=apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                    apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ᵣ'],
                        apply(
                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₊'],
                            premise_config(
                                main=parse_formula_with_substitution('(Sn = Sy)[y ↦ n]', ARITHMETIC_SIGNATURE),
                                tree=apply(
                                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['=₊'],
                                    instantiation=AtomicLogicSchemaInstantiation(
                                        term_mapping={
                                            parse_term_placeholder('τ'): parse_term('Sy', ARITHMETIC_SIGNATURE),
                                        },
                                    ),
                                ),
                            ),
                        ),
                        instantiation=AtomicLogicSchemaInstantiation(
                            formula_mapping={
                                parse_formula_placeholder('φ'): parse_formula('(Sn = 0)', ARITHMETIC_SIGNATURE),
                            },
                        ),
                    ),
                    instantiation=AtomicLogicSchemaInstantiation(
                        formula_mapping={
                            parse_formula_placeholder('φ'): substitute_in_formula(aux, {parse_variable('x'): parse_variable('n')}),
                        },
                    ),
                ),
            ),
        ),
    )

    assert str(tree) == dedent("""\
                                                             _________ =₊
                                                             (Sy = Sy)
                                                            ____________ ∃₊
                                                            ∃y.(Sn = Sy)
                                                      _________________________ ∨₊ᵣ
                                                      ((Sn = 0) ∨ ∃y.(Sn = Sy))
                _______ =₊              _____________________________________________________ →₊
                (0 = 0)                 (((n = 0) ∨ ∃y.(n = Sy)) → ((Sn = 0) ∨ ∃y.(Sn = Sy)))
        _______________________ ∨₊ₗ    ________________________________________________________ ∀₊
        ((0 = 0) ∨ ∃y.(0 = Sy))        ∀n.(((n = 0) ∨ ∃y.(n = Sy)) → ((Sn = 0) ∨ ∃y.(Sn = Sy)))
        _______________________________________________________________________________________ ∧₊
         (((0 = 0) ∨ ∃y.(0 = Sy)) ∧ ∀n.(((n = 0) ∨ ∃y.(n = Sy)) → ((Sn = 0) ∨ ∃y.(Sn = Sy))))
        """,
    )

    assert induction_axiom.left == tree.conclusion
