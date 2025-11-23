import pytest

from .parsing import parse_formula, parse_term
from .signature import FormalLogicSignature
from .signature_translation import SignatureTranslation, SignatureTranslationError, translate_formula, translate_term


def test_translation_kind_mismatch(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(SignatureTranslationError, match="Mismatch between the function symbol 'f¹' and the predicate symbol 'p¹'"):
        SignatureTranslation(dummy_signature, dummy_signature, {'f¹': 'p¹'})


def test_translation_arity_mismatch(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(SignatureTranslationError, match="Mismatch between 'f¹' of arity 1 and 'g²' of arity 2"):
        SignatureTranslation(dummy_signature, dummy_signature, {'f¹': 'g²'})


def test_translate_term(dummy_signature: FormalLogicSignature) -> None:
    target_signature = FormalLogicSignature()
    target_signature.add_symbol('FUNCTION', 'ф²', 2)
    target_signature.add_symbol('FUNCTION', 'г¹', 1)

    translation = SignatureTranslation(
        dummy_signature,
        target_signature,
        {'f²': 'ф²', 'g¹': 'г¹'}
    )

    term = parse_term('f²(g¹(x), y)', dummy_signature)
    assert str(translate_term(translation, term)) == 'ф²(г¹(x), y)'


def test_translate_formula(dummy_signature: FormalLogicSignature) -> None:
    target_signature = FormalLogicSignature()
    target_signature.add_symbol('FUNCTION', 'ф⁰', 0)
    target_signature.add_symbol('PREDICATE', 'п¹', 1)

    translation = SignatureTranslation(
        dummy_signature,
        target_signature,
        {'f⁰': 'ф⁰', 'p¹': 'п¹'}
    )

    formula = parse_formula('¬∃x.(p¹(x) → p¹(f⁰))', dummy_signature)
    assert str(translate_formula(translation, formula)) == '¬∃x.(п¹(x) → п¹(ф⁰))'
