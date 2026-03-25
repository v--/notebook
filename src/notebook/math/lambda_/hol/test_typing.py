from textwrap import dedent

from ..parsing import parse_variable_assertion
from ..type_derivation import apply, assume
from .signature import PLAIN_HOL_SIGNATURE
from .typing import BASE_HOL_TYPE_SYSTEM


def test_top() -> None:
    tree = apply(BASE_HOL_TYPE_SYSTEM['H⊤'])

    assert str(tree) == dedent('''\
        _____ H⊤
        H⊤: ο
        ''',
    )


def test_and() -> None:
    tree = apply(
        BASE_HOL_TYPE_SYSTEM['→₋'],
        apply(
            BASE_HOL_TYPE_SYSTEM['→₋'],
            apply(BASE_HOL_TYPE_SYSTEM['H∧']),
            assume(parse_variable_assertion('p: ο', PLAIN_HOL_SIGNATURE)),
        ),
        assume(parse_variable_assertion('q: ο', PLAIN_HOL_SIGNATURE)),
    )

    assert str(tree) == dedent('''\
        _________________ H∧
        H∧: (ο → (ο → ο))       p: ο
        ______________________________ →₋
                (H∧p): (ο → ο)               q: ο
        ___________________________________________ →₋
                        ((H∧p)q): ο
        ''',
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
        ''',
    )
