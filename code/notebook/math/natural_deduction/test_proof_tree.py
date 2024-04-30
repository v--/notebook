from textwrap import dedent

from ..fol.parsing import parse_propositional_formula
from .axiomatic_derivation import AxiomaticDerivation, derivation_to_proof_tree
from .minimal_implicational_logic import IMPLICATIONAL_AXIOMS, get_identity_derivation_payload
from .minimal_logic import minimal_nd_system
from .proof_tree import AssumptionTree, MarkedFormula, RuleApplicationTree
from .schemas import FormulaPlaceholder
from .substitution import UniformSubstitution


def test_assumption_tree() -> None:
    tree = AssumptionTree(
        minimal_nd_system,
        parse_propositional_formula('p'),
        marker='u'
    )

    assert set(tree.iter_open_assumptions()) == {
        MarkedFormula(parse_propositional_formula('p'), 'u')
    }

    assert str(tree) == dedent('''\
        [p]ᵘ
        '''
    )


def test_simple_rule_application_tree() -> None:
    substitution = UniformSubstitution({
        FormulaPlaceholder('φ'): parse_propositional_formula('p'),
        FormulaPlaceholder('ψ'): parse_propositional_formula('q')
    })

    tree = RuleApplicationTree(
        minimal_nd_system,
        rule=minimal_nd_system['→⁺'],
        substitution=substitution,
        subtrees=[
            RuleApplicationTree(
                minimal_nd_system,
                rule=minimal_nd_system['→⁻'],
                substitution=substitution,
                subtrees=[
                    AssumptionTree(
                        minimal_nd_system,
                        parse_propositional_formula('(p → q)'),
                        marker='u'
                    ),
                    AssumptionTree(
                        minimal_nd_system,
                        parse_propositional_formula('p'),
                        marker='v'
                    )
                ]
            )
        ]
    )

    assert set(tree.iter_open_assumptions()) == {
        MarkedFormula(parse_propositional_formula('(p → q)'), 'u')
    }

    assert str(tree) == dedent('''\
          [(p → q)]ᵘ    [p]ᵛ
          __________________ →⁻
                  q
        v _____________________ →⁺
                 (p → q)
        '''
    )


def test_complex_rule_application_tree() -> None:
    derivation = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=get_identity_derivation_payload(parse_propositional_formula('p'))
    )

    tree = derivation_to_proof_tree(derivation)

    assert set(tree.iter_open_assumptions()) == set()
    assert str(tree) == dedent('''\
        _________________________________________________ Ax    ___________________ Ax
        ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p)))       (p → ((p → p) → p))
        ______________________________________________________________________________ MP    _____________ Ax
                                  ((p → (p → p)) → (p → p))                                  (p → (p → p))
        _____________________________________________________________________________________________________ MP
                                                       (p → p)
        '''
    )
