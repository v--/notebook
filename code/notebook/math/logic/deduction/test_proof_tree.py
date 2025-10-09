import re
from collections.abc import Mapping
from textwrap import dedent

import pytest

from ..classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ..instantiation import FormalLogicSchemaInstantiation
from ..parsing import (
    parse_formula,
    parse_formula_placeholder,
    parse_marker,
    parse_propositional_formula,
    parse_substitution_spec,
)
from ..signature import FormalLogicSignature
from .exceptions import RuleApplicationError
from .proof_tree import AssumptionTree, ProofTree, RuleApplicationPremise, apply, assume, premise


def prop_assume(formula: str, marker: str) -> AssumptionTree:
    return assume(parse_propositional_formula(formula), parse_marker(marker))


def prop_premise(*, tree: ProofTree, discharge: str, marker: str | None = None) -> RuleApplicationPremise:
    return premise(
        tree=tree,
        discharge=parse_propositional_formula(discharge),
        marker=parse_marker(marker) if marker is not None else None
    )


def str_context(tree: ProofTree) -> Mapping[str, str]:
    return {str(marker): str(formula) for marker, formula in tree.get_assumption_map().items()}


def test_assumption_tree() -> None:
    tree = prop_assume('p', 'u')
    assert str_context(tree) == {'u': 'p'}
    assert str(tree) == dedent('''\
        [p]ᵘ
        '''
    )


def test_single_implication_intro() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        prop_premise(
            tree=prop_assume('q', 'u'),
            discharge='p'
        )
    )

    assert str_context(tree) == {'u': 'q'}
    assert str(tree) == dedent('''\
          [q]ᵘ
         _______ →₊
         (p → q)
        '''
    )


def test_double_implication_intro() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        prop_premise(
            marker='u',
            discharge='p',
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                prop_premise(
                    discharge='q',
                    tree=prop_assume('p', 'u')
                )
            ),
        )
    )

    assert str_context(tree) == {}
    assert str(tree) == dedent('''\
              [p]ᵘ
             _______ →₊
             (q → p)
        u _____________ →₊
          (p → (q → p))
        '''
    )


def test_efq() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['EFQ'],
        prop_assume('⊥', 'u'),
        # We are unable to infer the necessary instantiation of the rule "(EFQ) ⊥ ⫢ φ"
        # based only on the conclusion and premises, so we give a hint
        instantiation=FormalLogicSchemaInstantiation(
            formula_mapping={
                parse_formula_placeholder('φ'): parse_propositional_formula('p')
            }
        )
    )

    assert str_context(tree) == {'u': '⊥'}
    assert str(tree) == dedent('''\
        [⊥]ᵘ
        ____ EFQ
         p
        '''
    )


def test_implication_distributivity_axiom_tree() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        prop_premise(
            discharge='(p → (q → r))',
            marker='u',
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                prop_premise(
                    discharge='(p → q)',
                    marker='w',
                    tree=apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                        prop_premise(
                            discharge='p',
                            marker='v',
                            tree=apply(
                                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                                apply(
                                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                                    prop_assume('(p → (q → r))', 'u'),
                                    prop_assume('p', 'v')
                                ),
                                apply(
                                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                                    prop_assume('(p → q)', 'w'),
                                    prop_assume('p', 'v')
                                )
                            )
                        )
                    )
                )
            )
        )
    )

    assert str_context(tree) == {}
    assert str(tree) == dedent('''\
          [(p → (q → r))]ᵘ    [p]ᵛ       [(p → q)]ʷ    [p]ᵛ
          ________________________ →₋    __________________ →₋
                  (q → r)                        q
          _________________________________________________ →₋
                                  r
        v _________________________________________________ →₊
                               (p → r)
        w _________________________________________________ →₊
                         ((p → q) → (p → r))
        u _________________________________________________ →₊
                ((p → (q → r)) → ((p → q) → (p → r)))
        '''
    )


def test_invalid_application_arity() -> None:
    with pytest.raises(RuleApplicationError, match='The rule ∧₊ has 2 premises, but the application has 1'):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧₊'],
            prop_assume('p', 'u')
            # Should have one more premise
        )


def test_invalid_application_duplicate_marker() -> None:
    with pytest.raises(RuleApplicationError, match='Multiple assumptions cannot have the same marker'):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∧₊'],
            prop_assume('p', 'u'),
            prop_assume('q', 'u')
        )


def test_invalid_application_missing_discharge() -> None:
    with pytest.raises(RuleApplicationError, match='The rule →₊ requires a discharge formula for premise number 1'):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
            prop_assume('p', 'u'),
        )


def test_forall_introduction() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise(
            tree=apply(CLASSICAL_NATURAL_DEDUCTION_SYSTEM['⊤₊']),
            main_sub=parse_substitution_spec('x ↦ x'),
        ),
    )

    assert str(tree) == dedent('''\
        ________ ⊤₊
        ⊤[x ↦ x]
        ________ ∀₊
          ∀x.⊤
        '''
    )


def test_forall_reintroduction(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p₁(x)', dummy_signature), parse_marker('u')),
                conclusion_sub=parse_substitution_spec('x ↦ x'),
            ),
            main_sub=parse_substitution_spec('x ↦ x'),
        ),
    )

    assert str(tree) == dedent('''\
        [∀x.p₁(x)]ᵘ
        ____________ ∀₋
        p₁(x)[x ↦ x]
        ____________ ∀₊
          ∀x.p₁(x)
        '''
    )


def test_forall_to_exists(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₊'],
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p₁(x)', dummy_signature), parse_marker('u')),
                conclusion_sub=parse_substitution_spec('x ↦ x'),
            ),
            main_sub=parse_substitution_spec('x ↦ x'),
        ),
    )

    assert str(tree) == dedent('''\
        [∀x.p₁(x)]ᵘ
        ____________ ∀₋
        p₁(x)[x ↦ x]
        ____________ ∃₊
          ∃x.p₁(x)
        '''
    )


def test_forall_negation(dummy_signature: FormalLogicSignature) -> None:
    u = parse_formula('¬∃x.p₁(x)', dummy_signature)
    v = parse_formula('p₁(x)', dummy_signature)
    w = parse_formula('¬∀x.¬p₁(x)', dummy_signature)

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['DNE'],
                premise(
                    tree=apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['¬₋'],
                        assume(w, parse_marker('w')),
                        apply(
                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
                            premise(
                                tree=apply(
                                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['¬₊'],
                                    premise(
                                        tree=apply(
                                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['¬₋'],
                                            assume(u, parse_marker('u')),
                                            apply(
                                                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₊'],
                                                premise(
                                                    tree=assume(v, parse_marker('v')),
                                                    main_sub=parse_substitution_spec('x ↦ x'),
                                                ),
                                            )
                                        ),
                                        discharge=v
                                    )
                                ),
                                main_sub=parse_substitution_spec('x ↦ x'),
                            )
                        )
                    ),
                    discharge=u
                )
            ),
            discharge=w
        )
    )

    assert str(tree) == dedent('''\
                                             [p₁(x)]ᵛ[x ↦ x]
                                             _______________ ∃₊
                             [¬∃x.p₁(x)]ᵘ       ∃x.p₁(x)
                             _______________________________ ¬₋
                                            ⊥
                           v _______________________________ ¬₊
                                      ¬p₁(x)[x ↦ x]
                           _______________________________ ∀₊
          [¬∀x.¬p₁(x)]ʷ                 ∀x.¬p₁(x)
          __________________________________________________ ¬₋
                                  ⊥
        u __________________________________________________ DNE
                               ∃x.p₁(x)
        w __________________________________________________ →₊
                       (¬∀x.¬p₁(x) → ∃x.p₁(x))
        '''
    )


def test_forall_introduction_failure(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(RuleApplicationError, match=re.escape('The eigenvariable x cannot be free in the derivation of p₁(x)')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
            premise(
                tree=assume(
                    parse_formula('p₁(x)', dummy_signature),
                    parse_marker('u')
                ),
                main_sub=parse_substitution_spec('x ↦ x'),
            ),
        )
