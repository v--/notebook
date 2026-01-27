from textwrap import dedent

from ...classical_logic import CLASSICAL_NATURAL_DEDUCTION_SYSTEM
from ...deduction import MarkedFormula, apply, assume, premise_config
from ...parsing import parse_formula, parse_formula_placeholder, parse_marker
from ...signature import FormalLogicSignature
from ..parsing import parse_prop_formula, parse_prop_variable
from .proof_tree_application import translate_prop_proof_tree


def test_assumption_tree(dummy_signature: FormalLogicSignature) -> None:
    prop_tree = assume(parse_prop_formula('p'), parse_marker('u'))
    translated = translate_prop_proof_tree(
        prop_tree,
        {parse_prop_variable('p'): parse_formula('p²(x, y)', dummy_signature)}
    )

    assert str(translated) == dedent('''\
        [p²(x, y)]ᵘ
        '''
    )


def test_double_implication_intro(dummy_signature: FormalLogicSignature) -> None:
    prop_tree = apply(
        CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
        premise_config(
            attachments=[MarkedFormula(parse_prop_formula('p'), parse_marker('u'))],
            tree=apply(
                CLASSICAL_NATURAL_DEDUCTION_SYSTEM['→₊'],
                assume(parse_prop_formula('p'), parse_marker('u')),
                implicit={
                    parse_formula_placeholder('φ'): parse_prop_formula('q')
                }
            )
        )
    )

    translated = translate_prop_proof_tree(
        prop_tree,
        {
            parse_prop_variable('p'): parse_formula('p¹(x)', dummy_signature),
            parse_prop_variable('q'): parse_formula('q¹(x)', dummy_signature)
        }
    )

    assert str(translated) == dedent('''\
                  [p¹(x)]ᵘ
               _______________ →₊
               (q¹(x) → p¹(x))
        u _________________________ →₊
          (p¹(x) → (q¹(x) → p¹(x)))
        '''
    )

