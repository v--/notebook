from textwrap import dedent

from ..algebraic_types import SIMPLE_ALGEBRAIC_SIGNATURE, SIMPLE_ALGEBRAIC_TYPE_SYSTEM
from ..common import combinators, pairs
from ..erasure import erase_annotations
from ..instantiation import LambdaSchemaInstantiation
from ..parsing import parse_type, parse_type_placeholder, parse_variable_assertion
from .tree import apply, assume, premise


def test_assumption_tree() -> None:
    assumption = parse_variable_assertion('x: τ')
    tree = assume(assumption)
    assert tree.get_assumption_map() == {assumption.term: assumption.type}
    assert str(tree) == dedent('''\
        x: τ
        '''
    )


# ex:def:type_derivation_tree/i
def test_arrow_intro() -> None:
    assumption = parse_variable_assertion('x: τ')
    tree = apply(
        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₊'],
        premise(
            tree=assume(assumption),
            discharge=assumption
        )
    )

    assert tree.get_assumption_map() == {}
    assert str(tree) == dedent('''\
               x: τ
        x _________________ →₊
          (λx:τ.x): (τ → τ)
        '''
    )


# ex:def:type_derivation_tree/k
def test_nested_arrow_intro() -> None:
    assumption_x = parse_variable_assertion('x: τ')
    assumption_y = parse_variable_assertion('y: σ')
    tree = apply(
        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₊'],
        premise(
            discharge=assumption_x,
            tree=apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₊'],
                premise(
                    discharge=assumption_y,
                    tree=assume(assumption_x)
                )
            )
        )
    )

    assert tree.get_assumption_map() == {}
    assert erase_annotations(tree.conclusion.term) == combinators.k
    assert str(tree) == dedent('''\
                     x: τ
                _________________ →₊
                (λy:σ.x): (σ → τ)
        x ______________________________ →₊
          (λx:τ.(λy:σ.x)): (τ → (σ → τ))
        '''
    )


# ex:def:type_derivation_tree/pairs
def test_cons() -> None:
    assumption_f = parse_variable_assertion('f: (τ → (σ → ρ))')
    assumption_x = parse_variable_assertion('x: τ')
    assumption_y = parse_variable_assertion('y: σ')
    tree = apply(
        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₊'],
        premise(
            discharge=assumption_x,
            tree=apply(
                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₊'],
                premise(
                    discharge=assumption_y,
                    tree=apply(
                        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₊'],
                        premise(
                            discharge=assumption_f,
                            tree=apply(
                                SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₋'],
                                apply(
                                    SIMPLE_ALGEBRAIC_TYPE_SYSTEM['→₋'],
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

    assert tree.get_assumption_map() == {}
    assert erase_annotations(tree.conclusion.term) == pairs.cons

    assert str(tree) == dedent('''\
                         f: (τ → (σ → ρ))      x: τ
                         ____________________________ →₋
                                (fx): (σ → ρ)               y: σ
                         _________________________________________ →₋
                                        ((fx)y): ρ
                    f _______________________________________________ →₊
                      (λf:(τ → (σ → ρ)).((fx)y)): ((τ → (σ → ρ)) → ρ)
              y ____________________________________________________________ →₊
                (λy:σ.(λf:(τ → (σ → ρ)).((fx)y))): (σ → ((τ → (σ → ρ)) → ρ))
        x _________________________________________________________________________ →₊
          (λx:τ.(λy:σ.(λf:(τ → (σ → ρ)).((fx)y)))): (τ → (σ → ((τ → (σ → ρ)) → ρ)))
        '''
    )


def test_empty_elim() -> None:
    assumption = parse_variable_assertion('x: 0', SIMPLE_ALGEBRAIC_SIGNATURE)
    tree = apply(
        SIMPLE_ALGEBRAIC_TYPE_SYSTEM['0₋'],
        premise(
            tree=assume(assumption),
            discharge=assumption
        ),
        instantiation=LambdaSchemaInstantiation(
            type_mapping={
                parse_type_placeholder('τ'): parse_type('σ')
            }
        )
    )

    assert tree.get_assumption_map() == {}
    assert str(tree) == dedent('''\
           x: 0
        x ________ 0₋
          (E₋x): σ
        '''
    )
