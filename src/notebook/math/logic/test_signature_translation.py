import pytest

from .parsing import parse_formula, parse_term
from .signature import (
    FormalLogicSignature,
    FunctionSymbol,
    PredicateSymbol,
    SignatureMorphismError,
    SignatureSymbolNotation,
)
from .signature_translation import SignatureMorphism, translate_formula, translate_term


def test_translation_kind_mismatch(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(SignatureMorphismError, match='Mismatch between the function symbol f¹ and the predicate symbol p¹'):
        SignatureMorphism(dummy_signature, { dummy_signature['f¹']: dummy_signature['p¹'] })


def test_translation_arity_mismatch(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(SignatureMorphismError, match='Mismatch between the arity 1 of the function symbol f¹ and the arity 2 of the function symbol g²'):
        SignatureMorphism(dummy_signature, { dummy_signature['f¹']: dummy_signature['g²'] })


def test_translate_term(dummy_signature: FormalLogicSignature) -> None:
    target_signature = FormalLogicSignature()
    target_signature.add_symbol(FunctionSymbol('ф²', arity=2, notation=SignatureSymbolNotation.PREFIX))
    target_signature.add_symbol(FunctionSymbol('г¹', arity=1, notation=SignatureSymbolNotation.PREFIX))

    translation = SignatureMorphism(dummy_signature, {
        dummy_signature['f²']: target_signature['ф²'],
        dummy_signature['g¹']: target_signature['г¹']
    })

    term = parse_term('f²(g¹(x), y)', dummy_signature)
    assert str(translate_term(translation, term)) == 'ф²(г¹(x), y)'


def test_translate_term_exchange_prefix_and_infix(dummy_signature: FormalLogicSignature) -> None:
    translation = SignatureMorphism(dummy_signature, {
        dummy_signature['∘']: dummy_signature['f²'],
        dummy_signature['p²']: dummy_signature['≠'],
    })

    formula = parse_formula('p²(x, (y ∘ z))', dummy_signature)
    assert str(translate_formula(translation, formula)) == '(x ≠ f²(y, z))'


def xtest_translate_formula(dummy_signature: FormalLogicSignature) -> None:
    target_signature = FormalLogicSignature()
    target_signature.add_symbol(FunctionSymbol('ф⁰', 0, notation=SignatureSymbolNotation.CONDENSED))
    target_signature.add_symbol(PredicateSymbol('п¹', 1, notation=SignatureSymbolNotation.PREFIX))

    translation = SignatureMorphism(dummy_signature, {
        dummy_signature['f⁰']: target_signature['ф⁰'],
        dummy_signature['p¹']: target_signature['п¹']
    })

    formula = parse_formula('¬∃x.(p¹(x) → p¹(f⁰))', dummy_signature)
    assert str(translate_formula(translation, formula)) == '¬∃x.(п¹(x) → п¹(ф⁰))'
