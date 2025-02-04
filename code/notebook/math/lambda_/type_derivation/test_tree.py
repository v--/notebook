from textwrap import dedent

from ..common import combinators, pairs
from ..parsing import parse_variable_assertion
from ..signature import LambdaSignature
from ..type_systems import ARROW_ELIM_RULE_IMPLICIT, ARROW_INTRO_RULE_EXPLICIT, ARROW_INTRO_RULE_IMPLICIT
from .tree import RuleApplicationPremise, apply, assume


def test_assumption_tree(dummy_signature: LambdaSignature) -> None:
    assumption = parse_variable_assertion(dummy_signature, 'x: α')
    tree = assume(assumption)
    assert tree.get_context() == {assumption}
    assert str(tree) == dedent('''\
        x: α
        '''
    )


# ex:def:type_derivation_tree/i
def test_arrow_intro_untyped(dummy_signature: LambdaSignature) -> None:
    assumption = parse_variable_assertion(dummy_signature, 'x: α')
    tree = apply(
        ARROW_INTRO_RULE_IMPLICIT,
        RuleApplicationPremise(
            assume(assumption),
            discharge=assumption
        )
    )

    assert tree.get_context() == set()
    assert tree.conclusion.term == combinators.i
    assert str(tree) == dedent('''\
              x: α
        x _______________ →⁺
          (λx.x): (α → α)
        '''
    )


# ex:def:type_derivation_tree/i
def test_arrow_intro_typed(dummy_signature: LambdaSignature) -> None:
    assumption = parse_variable_assertion(dummy_signature, 'x: α')
    tree = apply(
        ARROW_INTRO_RULE_EXPLICIT,
        RuleApplicationPremise(
            assume(assumption),
            discharge=assumption
        )
    )

    assert tree.get_context() == set()
    assert str(tree) == dedent('''\
               x: α
        x _________________ →⁺
          (λx:α.x): (α → α)
        '''
    )


# ex:def:type_derivation_tree/k
def test_nested_arrow_intro(dummy_signature: LambdaSignature) -> None:
    assumption_x = parse_variable_assertion(dummy_signature, 'x: α')
    assumption_y = parse_variable_assertion(dummy_signature, 'y: β')
    tree = apply(
        ARROW_INTRO_RULE_IMPLICIT,
        RuleApplicationPremise(
            discharge=assumption_x,
            tree=apply(
                ARROW_INTRO_RULE_IMPLICIT,
                RuleApplicationPremise(
                    discharge=assumption_y,
                    tree=assume(assumption_x)
                )
            )
        )
    )

    assert tree.get_context() == set()
    assert tree.conclusion.term == combinators.k
    assert str(tree) == dedent('''\
                   x: α
               _______________ →⁺
               (λy.x): (β → α)
        x __________________________ →⁺
          (λx.(λy.x)): (α → (β → α))
        '''
    )


# ex:def:type_derivation_tree/pairs
def test_cons(dummy_signature: LambdaSignature) -> None:
    assumption_f = parse_variable_assertion(dummy_signature, 'f: (α → (β → γ))')
    assumption_x = parse_variable_assertion(dummy_signature, 'x: α')
    assumption_y = parse_variable_assertion(dummy_signature, 'y: β')
    tree = apply(
        ARROW_INTRO_RULE_IMPLICIT,
        RuleApplicationPremise(
            discharge=assumption_x,
            tree=apply(
                ARROW_INTRO_RULE_IMPLICIT,
                RuleApplicationPremise(
                    discharge=assumption_y,
                    tree=apply(
                        ARROW_INTRO_RULE_IMPLICIT,
                        RuleApplicationPremise(
                            discharge=assumption_f,
                            tree=apply(
                                ARROW_ELIM_RULE_IMPLICIT,
                                RuleApplicationPremise(
                                    tree=apply(
                                        ARROW_ELIM_RULE_IMPLICIT,
                                        RuleApplicationPremise(tree=assume(assumption_f)),
                                        RuleApplicationPremise(tree=assume(assumption_x))
                                    )
                                ),
                                RuleApplicationPremise(tree=assume(assumption_y))
                            )
                        )
                    )
                )
            )
        )
    )

    assert tree.get_context() == set()
    assert tree.conclusion.term == pairs.cons
    assert str(tree) == dedent('''\
                f: (α → (β → γ))      x: α
                ____________________________ →⁻
                       (fx): (β → γ)               y: β
                _________________________________________ →⁻
                               ((fx)y): γ
              f _________________________________________ →⁺
                    (λf.((fx)y)): ((α → (β → γ)) → γ)
             y ____________________________________________ →⁺
               (λy.(λf.((fx)y))): (β → ((α → (β → γ)) → γ))
        x _______________________________________________________ →⁺
          (λx.(λy.(λf.((fx)y)))): (α → (β → ((α → (β → γ)) → γ)))
        '''
    )
