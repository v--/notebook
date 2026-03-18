from textwrap import dedent

from notebook.math.lambda_.hol.signature import EMPTY_HOL_SIGNATURE

from ..parsing import parse_variable_assertion
from ..type_derivation import apply, assume
from .system import BASE_HOL_TYPE_SYSTEM


def test_top() -> None:
    tree = apply(BASE_HOL_TYPE_SYSTEM['H⊤'])

    assert str(tree) == dedent('''\
        _____ H⊤
        H⊤: ο
        '''
    )


def test_and() -> None:
    tree = apply(
        BASE_HOL_TYPE_SYSTEM['→₋'],
        apply(
            BASE_HOL_TYPE_SYSTEM['→₋'],
            apply(BASE_HOL_TYPE_SYSTEM['H∧']),
            assume(parse_variable_assertion('p: ο', EMPTY_HOL_SIGNATURE))
        ),
        assume(parse_variable_assertion('q: ο', EMPTY_HOL_SIGNATURE))
    )

    assert str(tree) == dedent('''\
        _________________ H∧
        H∧: (ο → (ο → ο))       p: ο
        ______________________________ →₋
                (H∧p): (ο → ο)               q: ο
        ___________________________________________ →₋
                        ((H∧p)q): ο
        '''
    )


def test_forall() -> None:
    tree = apply(
        BASE_HOL_TYPE_SYSTEM['H∀'],
        assume(parse_variable_assertion('x: ι')),
        apply(BASE_HOL_TYPE_SYSTEM['H⊤']),
    )

    assert str(tree) == dedent('''\
                  _____ H⊤
        x: ι      H⊤: ο
        ________________ H∀
        (H∀(λx:ι.H⊤)): ο
        '''
    )


def test_description() -> None:
    tree = apply(
        BASE_HOL_TYPE_SYSTEM['H℩'],
        assume(parse_variable_assertion('x: ι')),
        apply(BASE_HOL_TYPE_SYSTEM['H⊤']),
    )

    assert str(tree) == dedent('''\
                  _____ H⊤
        x: ι      H⊤: ο
        ________________ H℩
        (H℩(λx:ι.H⊤)): ι
        '''
    )
