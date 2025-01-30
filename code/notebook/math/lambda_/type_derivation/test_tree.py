from textwrap import dedent

from ..hol import ANDREWS_HOL, ANDREWS_HOL_SIGNATURE
from ..parsing import (
    parse_type_assertion,
)
from .tree import RuleApplicationPremise, apply, assume


def test_assumption_tree() -> None:
    assumption = parse_type_assertion(ANDREWS_HOL_SIGNATURE, 'x: ι')
    tree = assume(assumption)
    assert tree.get_context() == {assumption}
    assert str(tree) == dedent('''\
        x: ι
        '''
    )


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
    assert str(tree) == dedent('''\
                   x: ι
        (x: ι) _______________ Abs
               (λx.x): (ι → ι)
        '''
    )
