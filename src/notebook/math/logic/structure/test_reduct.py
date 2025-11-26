from ...rings.modular import Z5
from ..arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from ..groups import GROUP_ASSOCIATIVITY, GROUP_SIGNATURE
from ..signature import SignatureMorphism
from .formula_visitor import evaluate_formula
from .reduct import reduct_along_signature_morphism


def test_modular_reduct() -> None:
    morphism = SignatureMorphism(GROUP_SIGNATURE, {
        GROUP_SIGNATURE['1']: ARITHMETIC_SIGNATURE['0'],
        GROUP_SIGNATURE['~']: ARITHMETIC_SIGNATURE['~'],
        GROUP_SIGNATURE['⋅']: ARITHMETIC_SIGNATURE['+'],
    })

    structure = ModularArithmeticStructure(Z5)
    reduct = reduct_along_signature_morphism(morphism, structure)
    assert evaluate_formula(GROUP_ASSOCIATIVITY, reduct)
