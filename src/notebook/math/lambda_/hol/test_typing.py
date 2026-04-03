from textwrap import dedent

from ..parsing import parse_variable_assertion
from ..type_derivation import apply, assume
from .signature import PLAIN_HOL_SIGNATURE
from .typing import BASE_HOL_TYPE_SYSTEM


def test_top() -> None:
    tree = apply(BASE_HOL_TYPE_SYSTEM['L⊤'])

    assert str(tree) == dedent('''\
        _____ L⊤
        L⊤: ο
        ''',
    )


def test_and() -> None:
    tree = apply(
        BASE_HOL_TYPE_SYSTEM['→₋'],
        apply(
            BASE_HOL_TYPE_SYSTEM['→₋'],
            apply(BASE_HOL_TYPE_SYSTEM['L∧']),
            assume(parse_variable_assertion('p: ο', PLAIN_HOL_SIGNATURE)),
        ),
        assume(parse_variable_assertion('q: ο', PLAIN_HOL_SIGNATURE)),
    )

    assert str(tree) == dedent('''\
        _________________ L∧
        L∧: (ο → (ο → ο))       p: ο
        ______________________________ →₋
                (L∧p): (ο → ο)               q: ο
        ___________________________________________ →₋
                        ((L∧p)q): ο
        ''',
    )


def test_forall() -> None:
    tree = apply(
        BASE_HOL_TYPE_SYSTEM['L∀'],
        assume(parse_variable_assertion('x: ι')),
        apply(BASE_HOL_TYPE_SYSTEM['L⊤']),
    )

    assert str(tree) == dedent('''\
                  _____ L⊤
        x: ι      L⊤: ο
        ________________ L∀
        (L∀(λx:ι.L⊤)): ο
        ''',
    )
