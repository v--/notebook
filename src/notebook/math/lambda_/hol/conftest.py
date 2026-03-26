import pytest

from ...logic.conftest import dummy_signature  # noqa: F401
from ...logic.signature import (
    FormalLogicSignature,
    FunctionSymbol,
    SignatureMorphism,
)
from ...logic.structure import FormalLogicStructure, reduct_along_signature_morphism
from ...logic.theories.arithmetic import ARITHMETIC_SIGNATURE
from ...logic.theories.arithmetic import ModularArithmeticStructure as FolModularStructure
from ...rings.modular import Z3
from .modular import ModularArithmeticStructure as HolModularStructure


@pytest.fixture
def arithmetic_signature_morphism() -> SignatureMorphism:
    return SignatureMorphism(
        ARITHMETIC_SIGNATURE,
        {FunctionSymbol(name='S', arity=1): FunctionSymbol(name='S⁺', arity=1)},
    )


@pytest.fixture
def fol_z3_signature(arithmetic_signature_morphism: SignatureMorphism) -> FormalLogicSignature:
    return arithmetic_signature_morphism.get_modified_signature()


@pytest.fixture
def fol_z3_model(arithmetic_signature_morphism: SignatureMorphism) -> FormalLogicStructure:
    return reduct_along_signature_morphism(
        arithmetic_signature_morphism.get_reverse_morphism(),
        FolModularStructure(Z3),
    )


@pytest.fixture
def hol_z3_model() -> HolModularStructure:
    return HolModularStructure(Z3)
