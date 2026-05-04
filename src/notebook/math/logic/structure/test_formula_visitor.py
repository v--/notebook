from notebook.math.logic.signature import SignatureMorphism
from notebook.math.logic.signature_translation import translate_formula
from notebook.math.logic.theories.arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from notebook.math.logic.theories.groups import GROUP_ASSOCIATIVITY, GROUP_SIGNATURE
from notebook.math.rings.modular import Z5

from .formula_visitor import evaluate_formula


def test_z5_addition_associativity() -> None:
    morphism = SignatureMorphism(GROUP_SIGNATURE, {
        GROUP_SIGNATURE['⋅']: ARITHMETIC_SIGNATURE['+'],
    })

    addition_associativity = translate_formula(morphism, GROUP_ASSOCIATIVITY)
    structure = ModularArithmeticStructure(Z5)
    assert evaluate_formula(addition_associativity, structure)
