from textwrap import dedent

from ..parsing import parse_marker, parse_propositional_formula
from .classical_logic import classical_natural_deduction_system
from .markers import MarkedFormula
from .proof_tree import ProofTree, RuleApplicationPremise, apply, assume


def marked_prop_formula(formula: str, marker: str) -> MarkedFormula:
    return MarkedFormula(parse_propositional_formula(formula), parse_marker(marker))


def prop_rule_premise(*, subtree: ProofTree, discharge: str | None = None, marker: str | None = None) -> RuleApplicationPremise:
    return RuleApplicationPremise(
        subtree,
        parse_propositional_formula(discharge) if discharge else None,
        parse_marker(marker) if marker else None
    )


def test_assumption_tree() -> None:
    marked_assumption = marked_prop_formula('p', 'u')
    tree = assume(marked_prop_formula('p', 'u'))
    assert tree.get_context() == {marked_assumption}

    assert str(tree) == dedent('''\
        [p]ᵘ
        '''
    )


def test_single_implication_introduction() -> None:
    marked_assumption = marked_prop_formula('q', 'u')
    tree = apply(
        classical_natural_deduction_system['→⁺'],
        prop_rule_premise(discharge='p', subtree=assume(marked_assumption))
    )

    assert tree.get_context() == {marked_assumption}
    assert str(tree) == dedent('''\
          [q]ᵘ
         _______ →⁺
         (p → q)
        '''
    )


def test_double_implication_introduction() -> None:
    tree = apply(
        classical_natural_deduction_system['→⁺'],
        prop_rule_premise(
            discharge='p',
            marker='u',
            subtree=apply(
                classical_natural_deduction_system['→⁺'],
                prop_rule_premise(
                    discharge='q',
                    subtree=assume(
                        marked_prop_formula('p', 'u')
                    )
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
    tree = apply(
        classical_natural_deduction_system['→⁺'],
        prop_rule_premise(
            discharge='(p → (q → r))',
            marker='u',
            subtree=apply(
                classical_natural_deduction_system['→⁺'],
                prop_rule_premise(
                    discharge='(p → q)',
                    marker='w',
                    subtree=apply(
                        classical_natural_deduction_system['→⁺'],
                        prop_rule_premise(
                            discharge='p',
                            marker='v',
                            subtree=apply(
                                classical_natural_deduction_system['→⁻'],
                                prop_rule_premise(
                                    subtree=apply(
                                        classical_natural_deduction_system['→⁻'],
                                        prop_rule_premise(
                                            subtree=assume(marked_prop_formula('(p → (q → r))', 'u'))
                                        ),
                                        prop_rule_premise(
                                            subtree=assume(marked_prop_formula('p', 'v'))
                                        )
                                    )
                                ),
                                prop_rule_premise(
                                    subtree=apply(
                                        classical_natural_deduction_system['→⁻'],
                                        prop_rule_premise(
                                            subtree=assume(marked_prop_formula('(p → q)', 'w'))
                                        ),
                                        prop_rule_premise(
                                            subtree=assume(marked_prop_formula('p', 'v'))
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
