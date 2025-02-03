from textwrap import dedent

from ..common import combinators, pairs
from ..parsing import parse_variable_assertion
from ..signature import LambdaSignature
from ..type_systems import ABS_RULE_IMPLICIT, APP_RULE_IMPLICIT
from .tree import RuleApplicationPremise, apply, assume


TEST_SIGNATURE = LambdaSignature(base_types={'α', 'β', 'γ'}, constant_terms=set())


def test_assumption_tree() -> None:
    assumption = parse_variable_assertion(TEST_SIGNATURE, 'x: α')
    tree = assume(assumption)
    assert tree.get_context() == {assumption}
    assert str(tree) == dedent('''\
        x: α
        '''
    )


# ex:def:type_derivation_tree/i
def test_abs_application() -> None:
    assumption = parse_variable_assertion(TEST_SIGNATURE, 'x: α')
    tree = apply(
        ABS_RULE_IMPLICIT,
        RuleApplicationPremise(
            assume(assumption),
            discharge=assumption
        )
    )

    assert tree.get_context() == set()
    assert tree.conclusion.term == combinators.i
    assert str(tree) == dedent('''\
              x: α
        x _______________ Abs
          (λx.x): (α → α)
        '''
    )


# ex:def:type_derivation_tree/k
def test_nested_abs_application() -> None:
    assumption_x = parse_variable_assertion(TEST_SIGNATURE, 'x: α')
    assumption_y = parse_variable_assertion(TEST_SIGNATURE, 'y: β')
    tree = apply(
        ABS_RULE_IMPLICIT,
        RuleApplicationPremise(
            discharge=assumption_x,
            tree=apply(
                ABS_RULE_IMPLICIT,
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
               _______________ Abs
               (λy.x): (β → α)
        x __________________________ Abs
          (λx.(λy.x)): (α → (β → α))
        '''
    )


# ex:def:type_derivation_tree/pairs
def test_cons() -> None:
    assumption_f = parse_variable_assertion(TEST_SIGNATURE, 'f: (α → (β → γ))')
    assumption_x = parse_variable_assertion(TEST_SIGNATURE, 'x: α')
    assumption_y = parse_variable_assertion(TEST_SIGNATURE, 'y: β')
    tree = apply(
        ABS_RULE_IMPLICIT,
        RuleApplicationPremise(
            discharge=assumption_x,
            tree=apply(
                ABS_RULE_IMPLICIT,
                RuleApplicationPremise(
                    discharge=assumption_y,
                    tree=apply(
                        ABS_RULE_IMPLICIT,
                        RuleApplicationPremise(
                            discharge=assumption_f,
                            tree=apply(
                                APP_RULE_IMPLICIT,
                                RuleApplicationPremise(
                                    tree=apply(
                                        APP_RULE_IMPLICIT,
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
                ____________________________ App
                       (fx): (β → γ)                y: β
                __________________________________________ App
                                ((fx)y): γ
              f __________________________________________ Abs
                    (λf.((fx)y)): ((α → (β → γ)) → γ)
             y ____________________________________________ Abs
               (λy.(λf.((fx)y))): (β → ((α → (β → γ)) → γ))
        x _______________________________________________________ Abs
          (λx.(λy.(λf.((fx)y)))): (α → (β → ((α → (β → γ)) → γ)))
        '''
    )
