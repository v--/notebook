from textwrap import dedent

from ..common import combinators, pairs
from ..parsing import parse_variable_assertion
from ..signature import LambdaSignature
from ..type_systems import ARROW_ELIM_RULE_IMPLICIT, ARROW_INTRO_RULE_EXPLICIT, ARROW_INTRO_RULE_IMPLICIT
from .tree import apply, assume, premise


def test_assumption_tree(dummy_signature: LambdaSignature) -> None:
    assumption = parse_variable_assertion(dummy_signature, 'x: τ')
    tree = assume(assumption)
    assert tree.get_context() == {assumption.term: assumption.type}
    assert str(tree) == dedent('''\
        x: τ
        '''
    )


# ex:def:type_derivation_tree/i
def test_arrow_intro_untyped(dummy_signature: LambdaSignature) -> None:
    assumption = parse_variable_assertion(dummy_signature, 'x: τ')
    tree = apply(
        ARROW_INTRO_RULE_IMPLICIT,
        premise(
            tree=assume(assumption),
            discharge=assumption
        )
    )

    assert tree.get_context() == {}
    assert tree.conclusion.term == combinators.i
    assert str(tree) == dedent('''\
              x: τ
        x _______________ →⁺
          (λx.x): (τ → τ)
        '''
    )


# ex:def:type_derivation_tree/i
def test_arrow_intro_typed(dummy_signature: LambdaSignature) -> None:
    assumption = parse_variable_assertion(dummy_signature, 'x: τ')
    tree = apply(
        ARROW_INTRO_RULE_EXPLICIT,
        premise(
            tree=assume(assumption),
            discharge=assumption
        )
    )

    assert tree.get_context() == {}
    assert str(tree) == dedent('''\
               x: τ
        x _________________ →⁺
          (λx:τ.x): (τ → τ)
        '''
    )


# ex:def:type_derivation_tree/k
def test_nested_arrow_intro(dummy_signature: LambdaSignature) -> None:
    assumption_x = parse_variable_assertion(dummy_signature, 'x: τ')
    assumption_y = parse_variable_assertion(dummy_signature, 'y: σ')
    tree = apply(
        ARROW_INTRO_RULE_IMPLICIT,
        premise(
            discharge=assumption_x,
            tree=apply(
                ARROW_INTRO_RULE_IMPLICIT,
                premise(
                    discharge=assumption_y,
                    tree=assume(assumption_x)
                )
            )
        )
    )

    assert tree.get_context() == {}
    assert tree.conclusion.term == combinators.k
    assert str(tree) == dedent('''\
                   x: τ
               _______________ →⁺
               (λy.x): (σ → τ)
        x __________________________ →⁺
          (λx.(λy.x)): (τ → (σ → τ))
        '''
    )


# ex:def:type_derivation_tree/pairs
def test_cons(dummy_signature: LambdaSignature) -> None:
    assumption_f = parse_variable_assertion(dummy_signature, 'f: (τ → (σ → ρ))')
    assumption_x = parse_variable_assertion(dummy_signature, 'x: τ')
    assumption_y = parse_variable_assertion(dummy_signature, 'y: σ')
    tree = apply(
        ARROW_INTRO_RULE_IMPLICIT,
        premise(
            discharge=assumption_x,
            tree=apply(
                ARROW_INTRO_RULE_IMPLICIT,
                premise(
                    discharge=assumption_y,
                    tree=apply(
                        ARROW_INTRO_RULE_IMPLICIT,
                        premise(
                            discharge=assumption_f,
                            tree=apply(
                                ARROW_ELIM_RULE_IMPLICIT,
                                apply(
                                    ARROW_ELIM_RULE_IMPLICIT,
                                    assume(assumption_f),
                                    assume(assumption_x)
                                ),
                                assume(assumption_y)
                            )
                        )
                    )
                )
            )
        )
    )

    assert tree.get_context() == {}
    assert tree.conclusion.term == pairs.cons
    assert str(tree) == dedent('''\
              f: (τ → (σ → ρ))      x: τ
              ____________________________ →⁻
                     (fx): (σ → ρ)               y: σ
              _________________________________________ →⁻
                             ((fx)y): ρ
              _________________________________________ →⁺
                  (λf.((fx)y)): ((τ → (σ → ρ)) → ρ)
             ____________________________________________ →⁺
             (λy.(λf.((fx)y))): (σ → ((τ → (σ → ρ)) → ρ))
        _______________________________________________________ →⁺
        (λx.(λy.(λf.((fx)y)))): (τ → (σ → ((τ → (σ → ρ)) → ρ)))
        '''
    )
