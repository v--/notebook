from ...rings.modular import Z5
from ..signature import SignatureMorphism
from ..signature_translation import translate_formula
from ..theories.arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from ..theories.groups import GROUP_ASSOCIATIVITY, GROUP_SIGNATURE
from .formula_visitor import evaluate_formula


def test_z5_addition_associativity() -> None:
    morphism = SignatureMorphism(GROUP_SIGNATURE, {
        GROUP_SIGNATURE['⋅']: ARITHMETIC_SIGNATURE['+'],
    })

    addition_associativity = translate_formula(morphism, GROUP_ASSOCIATIVITY)
    structure = ModularArithmeticStructure(Z5)
    assert evaluate_formula(addition_associativity, structure)
