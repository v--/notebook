from textwrap import dedent

from ...classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...deduction.proof_tree import apply, assume, premise
from ...parsing import (
    parse_formula,
    parse_formula_with_substitution,
    parse_marker,
    parse_term_substitution_spec,
    parse_variable,
)
from .axioms import ABSORPTION_AXIOMS, COMMUTATIVITY_AXIOMS, EXTREMA_AXIOMS, INEQUALITY_COMPATIBILITY_AXIOMS
from .signature import BOOLEAN_ALGEBRA_SIGNATURE


def test_bottom_absorption_proof() -> None:
    top_axiom = EXTREMA_AXIOMS[1]
    comm_axiom = COMMUTATIVITY_AXIOMS[1]
    abs_axiom = ABSORPTION_AXIOMS[0]

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['=₋'],
                premise(
                    tree=apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                        premise(
                            tree=apply(
                                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                                assume(abs_axiom, parse_marker('u')),
                                conclusion_sub=parse_term_substitution_spec('x ↦ ⫫', BOOLEAN_ALGEBRA_SIGNATURE),
                            ),
                        ),
                        conclusion_sub=parse_term_substitution_spec('y ↦ x'),
                    ),
                    main=parse_formula_with_substitution('((⫫ ⩓ a) = ⫫)[a ↦ (⫫ ⩔ x)]', BOOLEAN_ALGEBRA_SIGNATURE),
                ),
                apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['=₋'],
                    premise(
                        tree=apply(
                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                            assume(top_axiom, parse_marker('v')),
                            conclusion_sub=parse_term_substitution_spec('x ↦ x'),
                        ),
                        main=parse_formula_with_substitution('(b = x)[b ↦ (x ⩔ ⫫)]', BOOLEAN_ALGEBRA_SIGNATURE),
                    ),
                    apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                        premise(
                            tree=apply(
                                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                                assume(comm_axiom, parse_marker('w')),
                                conclusion_sub=parse_term_substitution_spec('x ↦ x'),
                            ),
                        ),
                        conclusion_sub=parse_term_substitution_spec('y ↦ ⫫', BOOLEAN_ALGEBRA_SIGNATURE),
                    ),
                    conclusion_sub=parse_term_substitution_spec('b ↦ (⫫ ⩔ x)', BOOLEAN_ALGEBRA_SIGNATURE),
                ),
                conclusion_sub=parse_term_substitution_spec('a ↦ x'),
            ),
            main_noop_sub=parse_variable('x')
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
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['↔₋ₗ'],
                apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                    premise(
                        tree=apply(
                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                            assume(ineq_axiom, parse_marker('u')),
                            conclusion_sub=parse_term_substitution_spec('x ↦ ⫫', BOOLEAN_ALGEBRA_SIGNATURE),
                        ),
                    ),
                    conclusion_sub=parse_term_substitution_spec('y ↦ x'),
                ),
                apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                    assume(assumption, parse_marker('v')),
                    conclusion_sub=parse_term_substitution_spec('x ↦ x'),
                ),
            ),
            main_noop_sub=parse_variable('x')
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

