from textwrap import dedent

from ..fol.parsing import parse_formula
from ..fol.signature import FOLSignature
from .axiomatic_derivation import AxiomaticDerivation, derivation_to_proof_tree
from .minimal_implicational_logic import IMPLICATIONAL_AXIOMS, get_identity_derivation_payload
from .minimal_logic import minimal_nd_system
from .proof_tree import AssumptionTree, RuleApplicationTree
from .schemas import FormulaPlaceholder
from .substitution import UniformSubstitution


def test_assumption_tree_to_str(propositional_signature: FOLSignature) -> None:
    tree = AssumptionTree(
        minimal_nd_system,
        parse_formula(propositional_signature, 'p'),
        marker='u'
    )

    assert str(tree) == dedent('''\
        [p]ᵘ
        '''
    )


def test_simple_rule_application_tree_to_str(propositional_signature: FOLSignature) -> None:
    tree = RuleApplicationTree(
        minimal_nd_system,
        rule=minimal_nd_system['→⁺'],
        substitution=UniformSubstitution({
            FormulaPlaceholder('φ'): parse_formula(propositional_signature, 'p'),
            FormulaPlaceholder('ψ'): parse_formula(propositional_signature, 'q')
        }),
        subtrees=[
            AssumptionTree(
                minimal_nd_system,
                parse_formula(propositional_signature, 'p'),
                marker='u'
            ),
            AssumptionTree(
                minimal_nd_system,
                parse_formula(propositional_signature, 'q'),
                marker='v'
            )
        ]
    )

    assert str(tree) == dedent('''\
          [p]ᵘ    [q]ᵛ
        u ____________ →⁺
            (p → q)
        '''
    )


def test_complex_rule_application_tree_to_str(propositional_signature: FOLSignature) -> None:
    derivation = AxiomaticDerivation(
        axiom_schemas=IMPLICATIONAL_AXIOMS,
        payload=get_identity_derivation_payload(parse_formula(propositional_signature, 'p'))
    )

    tree = derivation_to_proof_tree(derivation)

    assert str(tree) == dedent('''\
        _________________________________________________ Ax    ___________________ Ax
        ((p → ((p → p) → p)) → ((p → (p → p)) → (p → p)))       (p → ((p → p) → p))
        ______________________________________________________________________________ MP    _____________ Ax
                                  ((p → (p → p)) → (p → p))                                  (p → (p → p))
        _____________________________________________________________________________________________________ MP
                                                       (p → p)
        '''
    )
