import re
from collections.abc import Collection, Mapping
from textwrap import dedent

import pytest

from ..classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ..instantiation import FormalLogicSchemaInstantiation
from ..parsing import (
    parse_formula,
    parse_formula_placeholder,
    parse_formula_with_substitution,
    parse_marker,
    parse_propositional_formula,
    parse_term_substitution_spec,
    parse_variable,
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


def str_assumptions(tree: ProofTree) -> Mapping[str, str]:
    return {str(marker): str(formula) for marker, formula in tree.get_assumption_map().items()}


def str_free_variables(tree: ProofTree) -> Collection[str]:
    return {str(var) for var in tree.get_free_variables()}


def test_assumption_tree() -> None:
    tree = prop_assume('p', 'u')
    assert str_assumptions(tree) == {'u': 'p'}
    assert str(tree) == dedent('''\
        [p]ᵘ
        '''
    )


def test_single_implication_intro() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        prop_premise(
            tree=prop_assume('q', 'u'),
            discharge='p',
            marker='u'
        )
    )

    assert str_assumptions(tree) == {'u': 'q'}
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

    assert str_assumptions(tree) == {}
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

    assert str_assumptions(tree) == {'u': '⊥'}
    assert str(tree) == dedent('''\
        [⊥]ᵘ
        ____ EFQ
         p
        '''
    )


# thm:minimal_implicational_logic_axioms_nd_proof
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

    assert str_assumptions(tree) == {}
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


# inf:thm:propositional_admissible_rules/self_biconditional
def test_self_biconditional() -> None:
    premise = prop_premise(
        marker='u',
        discharge='p',
        tree=prop_assume('p', 'u')
    )

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['↔₊'],
        premise,
        premise
    )

    assert str_assumptions(tree) == {}
    assert str(tree) == dedent('''\
          [p]ᵘ    [p]ᵘ
        u ____________ ↔₊
            (p ↔ p)
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
            main_noop_sub=parse_variable('x')
        ),
    )

    assert str(tree) == dedent('''\
         _ ⊤₊
         ⊤
        ____ ∀₊
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
                conclusion_sub=parse_term_substitution_spec('x ↦ x'),
            ),
            main_noop_sub=parse_variable('x')
        ),
    )

    assert str_free_variables(tree) == set()
    assert str(tree) == dedent('''\
        [∀x.p₁(x)]ᵘ
        ___________ ∀₋
           p₁(x)
        ___________ ∀₊
         ∀x.p₁(x)
        '''
    )


def test_forall_reintroduction_with_renaming(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p₁(x)', dummy_signature), parse_marker('u')),
                conclusion_sub=parse_term_substitution_spec('x ↦ y'),
            ),
            main=parse_formula_with_substitution('p₁(z)[z ↦ y]', dummy_signature),
        ),
    )

    assert str_free_variables(tree) == set()
    assert str(tree) == dedent('''\
                [∀x.p₁(x)]ᵘ
        ___________________________ ∀₋
        p₁(x)[x ↦ y] = p₁(z)[z ↦ y]
        ___________________________ ∀₊
                 ∀z.p₁(z)
        '''
    )


def test_forall_to_exists(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₊'],
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p₁(x)', dummy_signature), parse_marker('u')),
                conclusion_sub=parse_term_substitution_spec('x ↦ x'),
            ),
            main_noop_sub=parse_variable('x'),
        ),
    )

    assert str_free_variables(tree) == set()
    assert str(tree) == dedent('''\
        [∀x.p₁(x)]ᵘ
        ___________ ∀₋
           p₁(x)
        ___________ ∃₊
         ∃x.p₁(x)
        '''
    )


def test_forall_to_exists_with_constant(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₊'],
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p₁(x)', dummy_signature), parse_marker('u')),
                conclusion_sub=parse_term_substitution_spec('x ↦ f₀'),
            ),
            main=parse_formula_with_substitution('p₁(x)[x ↦ f₀]', dummy_signature)
        ),
    )

    assert str_free_variables(tree) == set()
    assert str(tree) == dedent('''\
         [∀x.p₁(x)]ᵘ
        _____________ ∀₋
        p₁(x)[x ↦ f₀]
        _____________ ∃₊
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
                                                    main_noop_sub=parse_variable('x')
                                                ),
                                            )
                                        ),
                                        discharge=v,
                                        marker=parse_marker('v')
                                    )
                                ),
                                main_noop_sub=parse_variable('x')
                            )
                        )
                    ),
                    discharge=u,
                    marker=parse_marker('u')
                )
            ),
            discharge=w,
            marker=parse_marker('w')
        )
    )

    assert str_free_variables(tree) == set()
    assert str(tree) == dedent('''\
                                             [p₁(x)]ᵛ
                                             ________ ∃₊
                             [¬∃x.p₁(x)]ᵘ    ∃x.p₁(x)
                             ________________________ ¬₋
                                        ⊥
                           v ________________________ ¬₊
                                      ¬p₁(x)
                           ________________________ ∀₊
          [¬∀x.¬p₁(x)]ʷ             ∀x.¬p₁(x)
          ___________________________________________ ¬₋
                               ⊥
        u ___________________________________________ DNE
                           ∃x.p₁(x)
        w ___________________________________________ →₊
                    (¬∀x.¬p₁(x) → ∃x.p₁(x))
        '''
    )


def test_forall_introduction_eigenvariable_failure_free_in_self(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(RuleApplicationError, match=re.escape('The renamed eigenvariable x ↦ y of the premise conclusion p₂(x, y) cannot be free in it')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
            premise(
                tree=assume(
                    parse_formula('p₂(x, y)', dummy_signature),
                    parse_marker('u')
                ),
                main=parse_formula_with_substitution('p₂(x, y)[x ↦ y]', dummy_signature)
            ),
        )


def test_forall_introduction_eigenvariable_failure_free_in_derivation(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(RuleApplicationError, match=re.escape('The eigenvariable x cannot be free in the derivation of p₁(x)')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
            premise(
                tree=assume(
                    parse_formula('p₁(x)', dummy_signature),
                    parse_marker('u')
                ),
                main_noop_sub=parse_variable('x')
            ),
        )


def test_exists_elimination(dummy_signature: FormalLogicSignature) -> None:
    u = parse_formula('∃x.p₁(x)', dummy_signature)
    v = parse_formula('∀y.(p₁(y) → q₁(f₀))', dummy_signature)
    w = parse_formula('p₁(y)', dummy_signature)

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₋'],
        assume(u, parse_marker('u')),
        premise(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                    assume(v, parse_marker('v')),
                    conclusion_sub=parse_term_substitution_spec('y ↦ y')
                ),
                assume(w, parse_marker('w')),  # We avoid discharging w here
            ),
            discharge=parse_formula_with_substitution('p₁(x)[x ↦ y]', dummy_signature),  # So that we can discharge it here
            marker=parse_marker('w')
        ),
    )

    assert str(tree) == dedent('''\
                         [∀y.(p₁(y) → q₁(f₀))]ᵛ
                         ______________________ ∀₋
                            (p₁(y) → q₁(f₀))          [p₁(y)]ʷ
                         _____________________________________ →₋
          [∃x.p₁(x)]ᵘ                   q₁(f₀)
        w ____________________________________________________ ∃₋
                                 q₁(f₀)
        '''
    )


def test_simple_invalid_exists_elimination(dummy_signature: FormalLogicSignature) -> None:
    u = parse_formula('∃x.p₁(x)', dummy_signature)
    v = parse_formula('p₁(y)', dummy_signature)

    # If not for its invalidity, the tree would look as follows:
    #
    #   [∃x.p₁(x)]ᵘ    [p₁(y)]ᵛ
    # v _______________________ ∃₋
    #            p₁(y)

    with pytest.raises(RuleApplicationError, match=re.escape('The discharge formula eigenvariable y cannot be free in the conclusion p₁(y) of premise number 2')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₋'],
            assume(u, parse_marker('u')),
            premise(
                tree=assume(v, parse_marker('v')),
                discharge=parse_formula_with_substitution('p₁(x)[x ↦ y]', dummy_signature),  # So that we can discharge it here
                marker=parse_marker('v')
            ),
        )


def test_invalid_exists_elimination_with_leftover_variable(dummy_signature: FormalLogicSignature) -> None:
    # A variation of test_exists_elimination with the constant f₀ replaced by the variable y
    u = parse_formula('∃x.p₁(x)', dummy_signature)
    v = parse_formula('∀y.(p₁(y) → q₁(y))', dummy_signature)
    w = parse_formula('p₁(y)', dummy_signature)

    # If not for its invalidity, the tree would look as follows:
    #
    #                  [∀y.(p₁(y) → q₁(y))]ᵛ
    #                  _____________________ ∀₋
    #                     (p₁(y) → q₁(y))          [p₁(y)]ʷ
    #                  ____________________________________ →₋
    #   [∃x.p₁(x)]ᵘ                   q₁(y)
    # w ___________________________________________________ ∃₋
    #                          q₁(y)

    with pytest.raises(RuleApplicationError, match=re.escape('The discharge formula eigenvariable y cannot be free in the conclusion q₁(y) of premise number 2')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₋'],
            assume(u, parse_marker('u')),
            premise(
                tree=apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                    apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                        assume(v, parse_marker('v')),
                        conclusion_sub=parse_term_substitution_spec('y ↦ y')
                    ),
                    assume(w, parse_marker('w')),  # We avoid discharging w here
                ),
                discharge=parse_formula_with_substitution('p₁(x)[x ↦ y]', dummy_signature),  # So that we can discharge it here
                marker=parse_marker('w')
            ),
        )


def test_invalid_exists_elimination_with_imprecise_quantification(dummy_signature: FormalLogicSignature) -> None:
    # A variation of test_exists_elimination without universal quantification
    u = parse_formula('∃x.p₁(x)', dummy_signature)
    v = parse_formula('(p₁(y) → q₁(f₀))', dummy_signature)
    w = parse_formula('p₁(y)', dummy_signature)

    # If not for its invalidity, the tree would look as follows:
    #
    #                  [(p₁(y) → q₁(f₀))]ᵛ    [p₁(y)]ʷ
    #                  _______________________________ →₋
    #   [∃x.p₁(x)]ᵘ                q₁(f₀)
    # w ______________________________________________ ∃₋
    #                       q₁(f₀)

    with pytest.raises(RuleApplicationError, match=re.escape('The eigenvariable y cannot be free in the derivation of q₁(f₀), except possibly in [p₁(x)[x ↦ y]]ʷ')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₋'],
            assume(u, parse_marker('u')),
            premise(
                tree=apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                    assume(v, parse_marker('v')),
                    assume(w, parse_marker('w')),  # We avoid discharging w here
                ),
                discharge=parse_formula_with_substitution('p₁(x)[x ↦ y]', dummy_signature),  # So that we can discharge it here
                marker=parse_marker('w')
            ),
        )
