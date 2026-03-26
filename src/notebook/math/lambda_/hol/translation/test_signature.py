from .....support.pytest import pytest_parametrize_kwargs
from ....logic.signature import FormalLogicSignature, FunctionSymbol, PredicateSymbol, SignatureSymbol
from ...parsing import parse_type
from ..modular import ARITHMETIC_SIGNATURE as HOL_ARITHMETIC_SIGNATURE
from ..signature import PLAIN_HOL_SIGNATURE
from .signature import fol_signature_to_hol_signature, fol_symbol_to_hol_type


@pytest_parametrize_kwargs(
    dict(fol_symbol=FunctionSymbol('0', 0), hol_type='ι'),
    dict(fol_symbol=FunctionSymbol('~', 1), hol_type='(ι → ι)'),
    dict(fol_symbol=PredicateSymbol('≤', 2), hol_type='(ι → (ι → ο))'),
    dict(fol_symbol=PredicateSymbol('p⁴', 4), hol_type='(ι → (ι → (ι → (ι → ο))))'),
)
def test_fol_symbol_to_hol_type(fol_symbol: SignatureSymbol, hol_type: str) -> None:
    hol_type_ = parse_type(hol_type, PLAIN_HOL_SIGNATURE)
    assert fol_symbol_to_hol_type(fol_symbol) == hol_type_


def test_fol_signature_to_hol_signature(fol_z3_signature: FormalLogicSignature) -> None:
    assert fol_signature_to_hol_signature(fol_z3_signature) == HOL_ARITHMETIC_SIGNATURE
