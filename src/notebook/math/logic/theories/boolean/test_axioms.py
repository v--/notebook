from textwrap import dedent

from ...classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...deduction.proof_tree import apply, assume, premise_config
from ...parsing import parse_formula, parse_formula_with_substitution, parse_marker
from .axioms import ABSORPTION_AXIOMS, COMMUTATIVITY_AXIOMS, EXTREMA_AXIOMS, INEQUALITY_COMPATIBILITY_AXIOMS
from .signature import BOOLEAN_ALGEBRA_SIGNATURE


def test_bottom_absorption_proof() -> None:
    top_axiom = EXTREMA_AXIOMS[1]
    comm_axiom = COMMUTATIVITY_AXIOMS[1]
    abs_axiom = ABSORPTION_AXIOMS[0]

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise_config(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['=₋'],
                premise_config(
                    main=parse_formula_with_substitution('((⫫ ⩓ a) = ⫫)[a ↦ (⫫ ⩔ x)]', BOOLEAN_ALGEBRA_SIGNATURE),
                    tree=apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                        apply(
                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                            assume(abs_axiom, parse_marker('u')),
                            conclusion_config=parse_formula_with_substitution('∀y.((x ⩓ (x ⩔ y)) = x)[x ↦ ⫫]', BOOLEAN_ALGEBRA_SIGNATURE),
                        ),
                        conclusion_config=parse_formula_with_substitution('((⫫ ⩓ (⫫ ⩔ y)) = ⫫)[y ↦ x]', BOOLEAN_ALGEBRA_SIGNATURE),
                    )
                ),
                apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['=₋'],
                    premise_config(
                        main=parse_formula_with_substitution('(b = x)[b ↦ (x ⩔ ⫫)]', BOOLEAN_ALGEBRA_SIGNATURE),
                        tree=apply(
                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                            assume(top_axiom, parse_marker('v')),
                            conclusion_config=parse_formula_with_substitution('((x ⩔ ⫫) = x)[x ↦ x]', BOOLEAN_ALGEBRA_SIGNATURE),
                        ),
                    ),
                    apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                        apply(
                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                            assume(comm_axiom, parse_marker('w')),
                            conclusion_config=parse_formula_with_substitution('∀y.((x ⩔ y) = (y ⩔ x))[x ↦ x]', BOOLEAN_ALGEBRA_SIGNATURE),
                        ),
                        conclusion_config=parse_formula_with_substitution('((x ⩔ y) = (y ⩔ x))[y ↦ ⫫]', BOOLEAN_ALGEBRA_SIGNATURE),
                    ),
                    conclusion_config=parse_formula_with_substitution('(b = x)[b ↦ (⫫ ⩔ x)]', BOOLEAN_ALGEBRA_SIGNATURE),
                ),
                conclusion_config=parse_formula_with_substitution('((⫫ ⩓ a) = ⫫)[a ↦ x]', BOOLEAN_ALGEBRA_SIGNATURE),
            ),
            main=parse_formula_with_substitution('((⫫ ⩓ x) = ⫫)[x ↦ x]', BOOLEAN_ALGEBRA_SIGNATURE)
        )
    )

    assert str(tree) == dedent('''\
                                                                     [∀x.∀y.((x ⩔ y) = (y ⩔ x))]ʷ
                                                                     ____________________________ ∀₋
        [∀x.∀y.((x ⩓ (x ⩔ y)) = x)]ᵘ       [∀x.((x ⩔ ⫫) = x)]ᵛ          ∀y.((x ⩔ y) = (y ⩔ x))
        ____________________________ ∀₋    ___________________ ∀₋    ____________________________ ∀₋
           ∀y.((⫫ ⩓ (⫫ ⩔ y)) = ⫫)             ((x ⩔ ⫫) = x)              ((x ⩔ ⫫) = (⫫ ⩔ x))
        ____________________________ ∀₋    ______________________________________________________ =₋
            ((⫫ ⩓ (⫫ ⩔ x)) = ⫫)                                ((⫫ ⩔ x) = x)
        _________________________________________________________________________________________ =₋
                                              ((⫫ ⩓ x) = ⫫)
        _________________________________________________________________________________________ ∀₊
                                            ∀x.((⫫ ⩓ x) = ⫫)
        '''
    )


def test_bottom_minimality_proof() -> None:
    # This was proven from axioms above
    assumption = parse_formula('∀x.((⫫ ⩓ x) = ⫫)', BOOLEAN_ALGEBRA_SIGNATURE)
    ineq_axiom = INEQUALITY_COMPATIBILITY_AXIOMS[0]

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise_config(
            main=parse_formula_with_substitution('(⫫ ≤ x)[x ↦ x]', BOOLEAN_ALGEBRA_SIGNATURE),
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['↔₋ₗ'],
                apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                    apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                        assume(ineq_axiom, parse_marker('u')),
                        conclusion_config=parse_formula_with_substitution('∀y.((x ≤ y) ↔ ((x ⩓ y) = x))[x ↦ ⫫]', BOOLEAN_ALGEBRA_SIGNATURE),
                    ),
                    conclusion_config=parse_formula_with_substitution('((⫫ ≤ y) ↔ ((⫫ ⩓ y) = ⫫))[y ↦ x]', BOOLEAN_ALGEBRA_SIGNATURE),
                ),
                apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                    assume(assumption, parse_marker('v')),
                    conclusion_config=parse_formula_with_substitution('((⫫ ⩓ x) = ⫫)[x ↦ x]', BOOLEAN_ALGEBRA_SIGNATURE),
                )
            ),
        ),
    )

    assert str(tree) == dedent('''\
        [∀x.∀y.((x ≤ y) ↔ ((x ⩓ y) = x))]ᵘ
        __________________________________ ∀₋
           ∀y.((⫫ ≤ y) ↔ ((⫫ ⩓ y) = ⫫))          [∀x.((⫫ ⩓ x) = ⫫)]ᵛ
        __________________________________ ∀₋    ___________________ ∀₋
            ((⫫ ≤ x) ↔ ((⫫ ⩓ x) = ⫫))               ((⫫ ⩓ x) = ⫫)
        ____________________________________________________________ ↔₋ₗ
                                  (⫫ ≤ x)
        ____________________________________________________________ ∀₊
                                 ∀x.(⫫ ≤ x)
        '''
    )
