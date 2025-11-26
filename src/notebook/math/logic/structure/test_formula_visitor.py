from ...rings.modular import Z5
from ..arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from ..groups import GROUP_ASSOCIATIVITY, GROUP_SIGNATURE
from ..signature_translation import SignatureMorphism, translate_formula
from .formula_visitor import evaluate_formula


def test_z5_addition_associativity() -> None:
    morphism = SignatureMorphism({
        GROUP_SIGNATURE.get_symbol('⋅'): ARITHMETIC_SIGNATURE.get_symbol('+'),
    })

    addition_associativity = translate_formula(morphism, GROUP_ASSOCIATIVITY)
    structure = ModularArithmeticStructure(Z5)
    assert evaluate_formula(addition_associativity, structure)
