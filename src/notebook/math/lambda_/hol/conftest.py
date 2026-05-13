from typing import TYPE_CHECKING

import pytest

from notebook.math.logic.conftest import dummy_signature  # noqa: F401
from notebook.math.logic.signature import FormalLogicSignature, FunctionSymbol, SignatureMorphism
from notebook.math.logic.structure import FormalLogicStructure, expand_along_signature_morphism
from notebook.math.logic.theories.arithmetic import ARITHMETIC_SIGNATURE as FOL_ARITHMETIC_SIGNATURE
from notebook.math.logic.theories.arithmetic import ModularArithmeticStructure as FolModularStructure
from notebook.math.rings.modular import Z3

from .theories.arithmetic import ARITHMETIC_SIGNATURE as HOL_ARITHMETIC_SIGNATURE
from .theories.arithmetic import ModularArithmeticStructure as HolModularStructure


if TYPE_CHECKING:
    from .signature import HolSignature


@pytest.fixture
def arithmetic_signature_morphism() -> SignatureMorphism:
    return SignatureMorphism(
        FOL_ARITHMETIC_SIGNATURE,
        {FunctionSymbol(name='S', arity=1): FunctionSymbol(name='S⁺', arity=1)},
    )


@pytest.fixture
def fol_z3_signature(arithmetic_signature_morphism: SignatureMorphism) -> FormalLogicSignature:
    return arithmetic_signature_morphism.get_modified_signature()


@pytest.fixture
def fol_z3_model(arithmetic_signature_morphism: SignatureMorphism) -> FormalLogicStructure[Z3]:
    return expand_along_signature_morphism(
        arithmetic_signature_morphism,
        FolModularStructure(Z3),
    )


@pytest.fixture
def hol_z3_signature() -> HolSignature:
    return HOL_ARITHMETIC_SIGNATURE


@pytest.fixture
def hol_z3_model() -> HolModularStructure:
    return HolModularStructure(Z3)
