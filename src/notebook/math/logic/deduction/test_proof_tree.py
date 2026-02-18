import re
from textwrap import dedent

import pytest

from ..classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ..parsing import (
    parse_formula,
    parse_formula_placeholder,
    parse_formula_with_substitution,
    parse_marker,
    parse_variable,
)
from ..propositional import parse_prop_formula
from ..formulas import NegationFormula
from ..signature import FormalLogicSignature
from .exceptions import RuleApplicationError
from .markers import MarkedFormula, MarkedFormulaWithSubstitution
from .proof_tree import AssumptionTree, apply, assume, premise_config


def prop_assume(formula: str, marker: str) -> AssumptionTree:
    return assume(parse_prop_formula(formula), parse_marker(marker))


def prop_marked_formula(formula: str, marker: str) -> MarkedFormula:
    return MarkedFormula(
        parse_prop_formula(formula),
        parse_marker(marker)
    )


def test_assumption_tree() -> None:
    tree = prop_assume('p', 'u')
    assert tree.get_cumulative_assumptions() == {prop_marked_formula('p', 'u')}
    assert str(tree) == dedent('''\
        [p]ᵘ
        '''
    )


def test_single_implication_intro() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        prop_assume('q', 'u'),
        implicit={
            parse_formula_placeholder('φ'): parse_prop_formula('p')
        }
    )

    assert tree.get_cumulative_assumptions() == {prop_marked_formula('q', 'u')}
    assert tree.get_local_implicit_open_premises() == {parse_prop_formula('p')}
    assert str(tree) == dedent('''\
          [q]ᵘ
         _______ →₊
         (p → q)
        '''
    )


def test_double_implication_intro() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        premise_config(
            attachments=[prop_marked_formula('p', 'u')],
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                prop_assume('p', 'u'),
                implicit={
                    parse_formula_placeholder('φ'): parse_prop_formula('q')
                }
            )
        )
    )

    assert tree.get_cumulative_assumptions() == set()
    assert tree.get_local_implicit_open_premises() == set()
    assert tree.premises[0].tree.get_local_implicit_open_premises() == {parse_prop_formula('q')}

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
        implicit={
            parse_formula_placeholder('φ'): parse_prop_formula('p')
        }
    )

    assert tree.get_cumulative_assumptions() == {prop_marked_formula('⊥', 'u')}
    assert tree.get_local_implicit_open_premises() == set()
    assert str(tree) == dedent('''\
        [⊥]ᵘ
        ____ EFQ
         p
        '''
    )


def test_or_intro() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∨₊ₗ'],
        prop_assume('p', 'u'),
        implicit={
            parse_formula_placeholder('ψ'): parse_prop_formula('q')
        }
    )

    assert tree.get_cumulative_assumptions() == {prop_marked_formula('p', 'u')}
    assert tree.get_local_implicit_open_premises() == {parse_prop_formula('q')}
    assert str(tree) == dedent('''\
         [p]ᵘ
        _______ ∨₊ₗ
        (p ∨ q)
        '''
    )


# ex:def:propositional_natural_deduction/efq_vs_dne
def test_dne() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        premise_config(
            attachments=[prop_marked_formula('¬¬p', 'u')],
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['RAA'],
                premise_config(
                    attachments=[prop_marked_formula('¬p', 'v')],
                    tree=apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['¬₋'],
                        prop_assume('¬¬p', 'u'),
                        prop_assume('¬p', 'v'),
                    ),
                )
            ),
        )
    )

    assert str(tree) == dedent('''\
          [¬¬p]ᵘ    [¬p]ᵛ
          _______________ ¬₋
                 ⊥
        v _______________ RAA
                 p
        u _______________ →₊
             (¬¬p → p)
        '''
    )


# thm:minimal_implicational_logic_axioms_nd_proof
def test_implication_distributivity_axiom_tree() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        premise_config(
            attachments=[prop_marked_formula('(p → (q → r))', 'u')],
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                premise_config(
                    attachments=[prop_marked_formula('(p → q)', 'w')],
                    tree=apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                        premise_config(
                            attachments=[prop_marked_formula('p', 'v')],
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
                            ),
                        )
                    ),
                )
            ),
        )
    )

    assert tree.get_cumulative_assumptions() == set()
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
    premise_ = premise_config(
        attachments=[prop_marked_formula('p', 'u')],
        tree=prop_assume('p', 'u'),
    )

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['↔₊'],
        premise_,
        premise_
    )

    assert tree.get_cumulative_assumptions() == set()
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


# ex:def:fol_natural_deduction/verum
def test_forall_introduction() -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise_config(
            tree=apply(CLASSICAL_NATURAL_DEDUCTION_SYSTEM['⊤₊']),
            main=parse_formula_with_substitution('⊤[x ↦ x]')
        ),
    )

    assert str(tree) == dedent('''\
         _ ⊤₊
         ⊤
        ____ ∀₊
        ∀x.⊤
        '''
    )


# rem:fol_empty_universe/natural_deduction
def test_forall_elimination(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
        assume(parse_formula('∀x.p¹(x)', dummy_signature), parse_marker('u')),
        conclusion_config=parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),
    )

    assert tree.get_open_variables() == set()
    assert tree.implicit_variables == {parse_variable('y')}
    assert str(tree) == dedent('''\
        [∀x.p¹(x)]ᵘ
        ___________ ∀₋
           p¹(y)
        '''
    )


# ex:def:fol_natural_deduction/reintroduction
def test_forall_reintroduction(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise_config(
            main=parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p¹(x)', dummy_signature), parse_marker('u')),
                conclusion_config=parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),
            ),
        )
    )

    assert tree.get_open_variables() == set()
    assert tree.implicit_variables == set()
    assert str(tree) == dedent('''\
        [∀x.p¹(x)]ᵘ
        ___________ ∀₋
           p¹(y)
        ___________ ∀₊
         ∀x.p¹(x)
        '''
    )


def test_forall_reintroduction_with_renaming(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
        premise_config(
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p¹(x)', dummy_signature), parse_marker('u')),
                conclusion_config=parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),
            ),
            main=parse_formula_with_substitution('p¹(z)[z ↦ y]', dummy_signature),
        ),
    )

    assert tree.get_open_variables() == set()
    assert tree.implicit_variables == set()
    assert str(tree) == dedent('''\
        [∀x.p¹(x)]ᵘ
        ___________ ∀₋
           p¹(y)
        ___________ ∀₊
         ∀z.p¹(z)
        '''
    )


def test_forall_to_exists(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₊'],
        premise_config(
            main=parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p¹(x)', dummy_signature), parse_marker('u')),
                conclusion_config=parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),
            ),
        )
    )

    assert tree.get_open_variables() == set()
    assert tree.implicit_variables == set()
    assert str(tree) == dedent('''\
        [∀x.p¹(x)]ᵘ
        ___________ ∀₋
           p¹(y)
        ___________ ∃₊
         ∃x.p¹(x)
        '''
    )


# ex:def:fol_natural_deduction/forall_to_exists
def test_forall_to_exists_with_constant(dummy_signature: FormalLogicSignature) -> None:
    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₊'],
        premise_config(
            main=parse_formula_with_substitution('p¹(x)[x ↦ f⁰]', dummy_signature),
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                assume(parse_formula('∀x.p¹(x)', dummy_signature), parse_marker('u')),
                conclusion_config=parse_formula_with_substitution('p¹(x)[x ↦ f⁰]', dummy_signature),
            )
        ),
    )

    assert tree.get_open_variables() == set()
    assert tree.implicit_variables == set()
    assert str(tree) == dedent('''\
        [∀x.p¹(x)]ᵘ
        ___________ ∀₋
          p¹(f⁰)
        ___________ ∃₊
         ∃x.p¹(x)
        '''
    )


# ex:def:fol_natural_deduction/quantifier_duality
def test_quantifier_duality(dummy_signature: FormalLogicSignature) -> None:
    u = parse_formula('¬∀x.¬p¹(x)', dummy_signature)
    v = parse_formula('¬∃x.p¹(x)', dummy_signature)
    w = parse_formula('p¹(x)', dummy_signature)

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        premise_config(
            attachments=[MarkedFormula(u, parse_marker('u'))],
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['RAA'],
                premise_config(
                    attachments=[MarkedFormula(v, parse_marker('v'))],
                    tree=apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['¬₋'],
                        assume(u, parse_marker('u')),
                        apply(
                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
                            premise_config(
                                main=parse_formula_with_substitution('¬p¹(x)[x ↦ x]', dummy_signature),
                                tree=apply(
                                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['¬₊'],
                                    premise_config(
                                        attachments=[MarkedFormula(w, parse_marker('w'))],
                                        tree=apply(
                                            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['¬₋'],
                                            assume(v, parse_marker('v')),
                                            apply(
                                                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₊'],
                                                premise_config(
                                                    tree=assume(w, parse_marker('w')),
                                                    main=parse_formula_with_substitution('p¹(x)[x ↦ x]', dummy_signature)
                                                ),
                                            )
                                        ),
                                    ),
                                ),
                            ),
                        )
                    ),
                ),
            ),
        )
    )

    assert tree.get_open_variables() == set()
    assert str(tree) == dedent('''\
                                             [p¹(x)]ʷ
                                             ________ ∃₊
                             [¬∃x.p¹(x)]ᵛ    ∃x.p¹(x)
                             ________________________ ¬₋
                                        ⊥
                           w ________________________ ¬₊
                                      ¬p¹(x)
                           ________________________ ∀₊
          [¬∀x.¬p¹(x)]ᵘ             ∀x.¬p¹(x)
          ___________________________________________ ¬₋
                               ⊥
        v ___________________________________________ RAA
                           ∃x.p¹(x)
        u ___________________________________________ →₊
                    (¬∀x.¬p¹(x) → ∃x.p¹(x))
        '''
    )


def test_forall_introduction_eigenvariable_failure_free_in_self(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(RuleApplicationError, match=re.escape('The eigenvariable y of the unsubstituted premise conclusion p²(x, y) cannot be free in it')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
            premise_config(
                tree=assume(
                    parse_formula('p²(x, y)', dummy_signature),
                    parse_marker('u')
                ),
                main=parse_formula_with_substitution('p²(x, y)[x ↦ y]', dummy_signature)
            ),
        )


# test_forall_introduction_eigenvariable_failure_free_in_implicit_premise
def test_forall_introduction_eigenvariable_failure_free_in_implicit_premise(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(RuleApplicationError, match=re.escape('The eigenvariable x cannot be free in the derivation of (p¹(x) → q¹(y))')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
            premise_config(
                tree=apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                    assume(
                        parse_formula('q¹(y)', dummy_signature),
                        parse_marker('u')
                    ),
                    implicit={
                        parse_formula_placeholder('φ'): parse_formula('p¹(x)', dummy_signature)
                    }
                ),
                main=parse_formula_with_substitution('(p¹(x) → q¹(y))[x ↦ x]', dummy_signature)
            ),
        )


def test_forall_introduction_eigenvariable_failure_free_in_derivation(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(RuleApplicationError, match=re.escape('The eigenvariable x cannot be free in the derivation of p¹(x)')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₊'],
            premise_config(
                tree=assume(
                    parse_formula('p¹(x)', dummy_signature),
                    parse_marker('u')
                ),
                main=parse_formula_with_substitution('p¹(x)[x ↦ x]', dummy_signature)
            ),
        )


# ex:def:fol_natural_deduction/exists_elimination
def test_exists_elimination(dummy_signature: FormalLogicSignature) -> None:
    u = parse_formula('∃x.p¹(x)', dummy_signature)
    v = parse_formula('∀y.(p¹(y) → q¹(z))', dummy_signature)
    w = parse_formula('p¹(y)', dummy_signature)

    tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₋'],
        assume(u, parse_marker('u')),
        premise_config(
            attachments=[
                MarkedFormulaWithSubstitution(
                    parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),  # So that we can discharge it here
                    parse_marker('w')
                )
            ],
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                    assume(v, parse_marker('v')),
                    conclusion_config=parse_formula_with_substitution('(p¹(y) → q¹(z))[y ↦ y]', dummy_signature)
                ),
                assume(w, parse_marker('w')),  # We avoid discharging w here
            ),
        ),
    )

    assert str(tree) == dedent('''\
                         [∀y.(p¹(y) → q¹(z))]ᵛ
                         _____________________ ∀₋
                            (p¹(y) → q¹(z))          [p¹(y)]ʷ
                         ____________________________________ →₋
          [∃x.p¹(x)]ᵘ                   q¹(z)
        w ___________________________________________________ ∃₋
                                 q¹(z)
        '''
    )


def test_simple_invalid_exists_elimination(dummy_signature: FormalLogicSignature) -> None:
    u = parse_formula('∃x.p¹(x)', dummy_signature)
    v = parse_formula('p¹(y)', dummy_signature)

    # If not for its invalidity, the tree would look as follows:
    #
    #   [∃x.p¹(x)]ᵘ    [p¹(y)]ᵛ
    # v _______________________ ∃₋
    #            p¹(y)

    with pytest.raises(RuleApplicationError, match=re.escape('The attached formula eigenvariable y cannot be free in the conclusion p¹(y) of premise number 2 of the rule ∃₋')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₋'],
            assume(u, parse_marker('u')),
            premise_config(
                tree=assume(v, parse_marker('v')),
                attachments=[
                    MarkedFormulaWithSubstitution(
                        parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),  # So that we can discharge it here
                        parse_marker('v')
                    )
                ]
            ),
        )


def test_invalid_exists_elimination_with_leftover_variable(dummy_signature: FormalLogicSignature) -> None:
    # A variation of test_exists_elimination with the constant f replaced by the variable y
    u = parse_formula('∃x.p¹(x)', dummy_signature)
    v = parse_formula('∀y.(p¹(y) → q¹(y))', dummy_signature)
    w = parse_formula('p¹(y)', dummy_signature)

    # If not for its invalidity, the tree would look as follows:
    #
    #                  [∀y.(p¹(y) → q¹(y))]ᵛ
    #                  _____________________ ∀₋
    #                     (p¹(y) → q¹(y))          [p¹(y)]ʷ
    #                  ____________________________________ →₋
    #   [∃x.p¹(x)]ᵘ                   q¹(y)
    # w ___________________________________________________ ∃₋
    #                          q¹(y)

    with pytest.raises(RuleApplicationError, match=re.escape('The attached formula eigenvariable y cannot be free in the conclusion q¹(y) of premise number 2 of the rule ∃₋')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₋'],
            assume(u, parse_marker('u')),
            premise_config(
                attachments=[
                    MarkedFormulaWithSubstitution(
                        parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),  # So that we can discharge it here
                        parse_marker('w')
                    )
                ],
                tree=apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                    apply(
                        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∀₋'],
                        assume(v, parse_marker('v')),
                        conclusion_config=parse_formula_with_substitution('(p¹(y) → q¹(y))[y ↦ y]', dummy_signature)
                    ),
                    assume(w, parse_marker('w')),  # We avoid discharging w here
                ),
            ),
        )


def test_invalid_exists_elimination_with_imprecise_quantification(dummy_signature: FormalLogicSignature) -> None:
    # A variation of test_exists_elimination without universal quantification
    u = parse_formula('∃x.p¹(x)', dummy_signature)
    v = parse_formula('(p¹(y) → q¹(f))', dummy_signature)
    w = parse_formula('p¹(y)', dummy_signature)

    # If not for its invalidity, the tree would look as follows:
    #
    #                  [(p¹(y) → q¹(f))]ᵛ    [p¹(y)]ʷ
    #                  _______________________________ →₋
    #   [∃x.p¹(x)]ᵘ                q¹(f)
    # w ______________________________________________ ∃₋
    #                       q¹(f)

    with pytest.raises(RuleApplicationError, match=re.escape('The eigenvariable y cannot be free in the derivation of q¹(f), except possibly in [p¹(y)]ʷ')):
        apply(
            CLASSICAL_NATURAL_DEDUCTION_SYSTEM['∃₋'],
            assume(u, parse_marker('u')),
            premise_config(
                attachments=[
                    MarkedFormulaWithSubstitution(
                        parse_formula_with_substitution('p¹(x)[x ↦ y]', dummy_signature),  # So that we can discharge it here
                        parse_marker('w')
                    )
                ],
                tree=apply(
                    CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₋'],
                    assume(v, parse_marker('v')),
                    assume(w, parse_marker('w')),  # We avoid discharging w here
                ),
            ),
        )
