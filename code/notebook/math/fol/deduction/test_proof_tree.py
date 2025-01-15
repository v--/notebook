from textwrap import dedent

from ..derivation.axiomatic_derivation import AxiomaticDerivation, derivation_to_proof_tree
from ..derivation.minimal_implicational_logic import IMPLICATIONAL_AXIOMS, get_identity_derivation_payload
from ..parsing import parse_marker, parse_propositional_formula
from .markers import MarkedFormula
from .propositional import propositional_apply, propositional_assume


def test_assumption_tree() -> None:
    tree = propositional_assume('p', 'u')

    assert set(tree.iter_open_assumptions()) == {
        MarkedFormula(parse_propositional_formula('p'), parse_marker('u'))
    }

    assert str(tree) == dedent('''\
        [p]ᵘ
        '''
    )


def test_implication_introduction_axiom_tree() -> None:
    tree = propositional_apply(
        '→⁺',
        propositional_apply(
            '→⁺',
            propositional_assume('p', 'u'),
            φ='q'
        ),
        φ='p'
    )

    assert set(tree.iter_open_assumptions()) == set()
    assert str(tree) == dedent('''\
              [p]ᵘ
             _______ →⁺
             (q → p)
        u _____________ →⁺
          (p → (q → p))
        '''
    )


def test_implication_distributivity_axiom_tree() -> None:
    tree = propositional_apply(
        '→⁺',
        propositional_apply(
            '→⁺',
            propositional_apply(
                '→⁺',
                propositional_apply(
                    '→⁻',
                    propositional_apply(
                        '→⁻',
                        propositional_assume('(p → (q → r))', 'u'),
                        propositional_assume('p', 'v')
                    ),
                    propositional_apply(
                        '→⁻',
                        propositional_assume('(p → q)', 'w'),
                        propositional_assume('p', 'v')
                    )
                ),
                φ='p'
            ),
            φ='(p → q)'
        ),
        φ='(p → (q → r))'
    )

    assert set(tree.iter_open_assumptions()) == set()
    assert str(tree) == dedent('''\
          [(p → (q → r))]ᵘ    [p]ᵛ       [(p → q)]ʷ    [p]ᵛ
          ________________________ →⁻    __________________ →⁻
                  (q → r)                        q
          _________________________________________________ →⁻
                                  r
        v _________________________________________________ →⁺
                               (p → r)
        w _________________________________________________ →⁺
                         ((p → q) → (p → r))
        u _________________________________________________ →⁺
                ((p → (q → r)) → ((p → q) → (p → r)))
        '''
    )


def test_implicational_identity_tree() -> None:
    derivation = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=get_identity_derivation_payload(parse_propositional_formula('p'))
    )

    tree = derivation_to_proof_tree(derivation)

    assert set(tree.iter_open_assumptions()) == set()
    assert str(tree) == dedent('''\
        _________________________________________________ Ax    ___________________ Ax
        ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p)))       (p → ((p → p) → p))
        ___________________________________________________________________________ MP    _____________ Ax
                                 ((p → (p → p)) → (p → p))                                (p → (p → p))
        _______________________________________________________________________________________________ MP
                                                    (p → p)
        '''
    )
