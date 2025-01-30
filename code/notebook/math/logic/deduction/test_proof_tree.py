from textwrap import dedent

from ..derivation.axiomatic_derivation import AxiomaticDerivation, derivation_to_proof_tree
from ..derivation.minimal_implicational_logic import IMPLICATIONAL_AXIOMS, get_identity_derivation_payload
from ..parsing import parse_marker, parse_propositional_formula
from .classical_logic import classical_natural_deduction_system
from .markers import MarkedFormula
from .proof_tree import AssumptionTree, ProofTree, RuleApplicationPremise, RuleApplicationTree, apply
from .rules import NaturalDeductionRule


def prop_assume(formula: str, marker: str) -> AssumptionTree:
    return AssumptionTree(MarkedFormula(parse_propositional_formula(formula), parse_marker(marker)))


def prop_rule_premise(*, subtree: ProofTree, discharge: str | None = None) -> RuleApplicationPremise:
    if discharge is None:
        return RuleApplicationPremise(subtree, None)

    return RuleApplicationPremise(subtree, parse_propositional_formula(discharge))


def prop_apply(rule: NaturalDeductionRule, *premises: RuleApplicationPremise) -> RuleApplicationTree:
    return apply(rule, *premises)


def test_assumption_tree() -> None:
    tree = prop_assume('p', 'u')
    assert tree.get_context() == {tree.marked_assumption}

    assert str(tree) == dedent('''\
        [p]ᵘ
        '''
    )


def test_single_implication_introduction() -> None:
    assumption_tree = prop_assume('q', 'u')
    tree = prop_apply(
        classical_natural_deduction_system['→⁺'],
        prop_rule_premise(discharge='p', subtree=assumption_tree)
    )

    assert tree.get_context() == {assumption_tree.marked_assumption}
    assert str(tree) == dedent('''\
          [q]ᵘ
         _______ →⁺
         (p → q)
        '''
    )


def test_double_implication_introduction() -> None:
    tree = prop_apply(
        classical_natural_deduction_system['→⁺'],
        prop_rule_premise(
            discharge='p',
            subtree=prop_apply(
                classical_natural_deduction_system['→⁺'],
                prop_rule_premise(
                    discharge='q',
                    subtree=prop_assume('p', 'u')
                )
            ),
        )
    )

    assert tree.get_context() == set()
    assert str(tree) == dedent('''\
              [p]ᵘ
             _______ →⁺
             (q → p)
        u _____________ →⁺
          (p → (q → p))
        '''
    )


def test_implication_distributivity_axiom_tree() -> None:
    tree = prop_apply(
        classical_natural_deduction_system['→⁺'],
        prop_rule_premise(
            discharge='(p → (q → r))',
            subtree=prop_apply(
                classical_natural_deduction_system['→⁺'],
                prop_rule_premise(
                    discharge='(p → q)',
                    subtree=prop_apply(
                        classical_natural_deduction_system['→⁺'],
                        prop_rule_premise(
                            discharge='p',
                            subtree=prop_apply(
                                classical_natural_deduction_system['→⁻'],
                                prop_rule_premise(
                                    subtree=prop_apply(
                                        classical_natural_deduction_system['→⁻'],
                                        prop_rule_premise(
                                            subtree=prop_assume('(p → (q → r))', 'u')
                                        ),
                                        prop_rule_premise(
                                            subtree=prop_assume('p', 'v')
                                        )
                                    )
                                ),
                                prop_rule_premise(
                                    subtree=prop_apply(
                                        classical_natural_deduction_system['→⁻'],
                                        prop_rule_premise(
                                            subtree=prop_assume('(p → q)', 'w')
                                        ),
                                        prop_rule_premise(
                                            subtree=prop_assume('p', 'v')
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )

    assert tree.get_context() == set()
    assert str(tree) == dedent('''\
          [(p → (q → r))]ᵘ    [p]ᵛ       [(p → q)]ʷ    [p]ᵛ
          ________________________ →⁻    __________________ →⁻
                  (q → r)                        q
          _________________________________________________ →⁻
                                  r
        v _________________________________________________ →⁺
                               (p → r)
        w _________________________________________________ →⁺
                         ((p → q) → (p → r))
        u _________________________________________________ →⁺
                ((p → (q → r)) → ((p → q) → (p → r)))
        '''
    )


def test_implicational_identity_tree() -> None:
    derivation = AxiomaticDerivation(
        payload=get_identity_derivation_payload(parse_propositional_formula('p'))
    )

    tree = derivation_to_proof_tree(IMPLICATIONAL_AXIOMS, derivation)

    assert tree.get_context() == set()
    assert str(tree) == dedent('''\
        _________________________________________________ Ax    ___________________ Ax
        ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p)))       (p → ((p → p) → p))
        ___________________________________________________________________________ MP    _____________ Ax
                                 ((p → (p → p)) → (p → p))                                (p → (p → p))
        _______________________________________________________________________________________________ MP
                                                    (p → p)
        '''
    )
