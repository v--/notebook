from ...rings.modular import Z5
from ..signature import SignatureMorphism
from ..theories.arithmetic import ARITHMETIC_SIGNATURE, ModularArithmeticStructure
from ..theories.groups import GROUP_ASSOCIATIVITY, GROUP_SIGNATURE
from .formula_visitor import evaluate_formula
from .reduction import reduce_along_signature_morphism


def test_reduce_along_signature_morphism_modular() -> None:
    morphism = SignatureMorphism(GROUP_SIGNATURE, {
        GROUP_SIGNATURE['𝕖']: ARITHMETIC_SIGNATURE['0'],
        GROUP_SIGNATURE['~']: ARITHMETIC_SIGNATURE['~'],
        GROUP_SIGNATURE['⋅']: ARITHMETIC_SIGNATURE['+'],
    })

    structure = ModularArithmeticStructure(Z5)
    reduct = reduce_along_signature_morphism(morphism, structure)
    assert evaluate_formula(GROUP_ASSOCIATIVITY, reduct)
