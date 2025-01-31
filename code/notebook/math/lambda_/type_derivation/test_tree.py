from textwrap import dedent

from ..hol import ANDREWS_HOL, ANDREWS_HOL_SIGNATURE
from ..parsing import (
    parse_type_assertion,
)
from .tree import RuleApplicationPremise, apply, assume
from ..common import combinators


def test_assumption_tree() -> None:
    assumption = parse_type_assertion(ANDREWS_HOL_SIGNATURE, 'x: ι')
    tree = assume(assumption)
    assert tree.get_context() == {assumption}
    assert str(tree) == dedent('''\
        x: ι
        '''
    )


# ex:def:type_derivation_tree/i
def test_abs_application() -> None:
    assumption = parse_type_assertion(ANDREWS_HOL_SIGNATURE, 'x: ι')
    tree = apply(
        ANDREWS_HOL['Abs'],
        RuleApplicationPremise(
            assume(assumption),
            discharge=assumption
        )
    )

    assert tree.get_context() == set()
    assert tree.conclusion.term == combinators.i
    assert str(tree) == dedent('''\
                   x: ι
        [x: ι] _______________ Abs
               (λx.x): (ι → ι)
        '''
    )


# ex:def:type_derivation_tree/k
def test_nested_abs_application() -> None:
    assumption_x = parse_type_assertion(ANDREWS_HOL_SIGNATURE, 'x: ι')
    assumption_y = parse_type_assertion(ANDREWS_HOL_SIGNATURE, 'y: o')
    tree = apply(
        ANDREWS_HOL['Abs'],
        RuleApplicationPremise(
            discharge=assumption_x,
            tree=apply(
                ANDREWS_HOL['Abs'],
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
                        x: ι
             [y: o] _______________ Abs
                    (λy.x): (o → ι)
        [x: ι] __________________________ Abs
               (λx.(λy.x)): (ι → (o → ι))
        '''
    )
