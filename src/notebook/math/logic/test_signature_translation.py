import pytest

from .parsing import parse_formula, parse_term
from .signature import FormalLogicSignature
from .signature_translation import SignatureTranslation, SignatureTranslationError, translate_formula, translate_term


def test_translation_kind_mismatch(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(SignatureTranslationError, match="Mismatch between the function symbol 'f₁' and the predicate symbol 'p₁'"):
        SignatureTranslation(dummy_signature, dummy_signature, {'f₁': 'p₁'})


def test_translation_arity_mismatch(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(SignatureTranslationError, match="Mismatch between 'f₁' of arity 1 and 'g₂' of arity 2"):
        SignatureTranslation(dummy_signature, dummy_signature, {'f₁': 'g₂'})


def test_translate_term(dummy_signature: FormalLogicSignature) -> None:
    target_signature = FormalLogicSignature()
    target_signature.add_symbol('FUNCTION', 'ф₂', 2)
    target_signature.add_symbol('FUNCTION', 'г₁', 1)

    translation = SignatureTranslation(
        dummy_signature,
        target_signature,
        {'f₂': 'ф₂', 'g₁': 'г₁'}
    )

    term = parse_term('f₂(g₁(x), y)', dummy_signature)
    assert str(translate_term(translation, term)) == 'ф₂(г₁(x), y)'


def test_translate_formula(dummy_signature: FormalLogicSignature) -> None:
    target_signature = FormalLogicSignature()
    target_signature.add_symbol('FUNCTION', 'ф₀', 0)
    target_signature.add_symbol('PREDICATE', 'п₁', 1)

    translation = SignatureTranslation(
        dummy_signature,
        target_signature,
        {'f₀': 'ф₀', 'p₁': 'п₁'}
    )

    formula = parse_formula('¬∃x.(p₁(x) → p₁(f₀))', dummy_signature)
    assert str(translate_formula(translation, formula)) == '¬∃x.(п₁(x) → п₁(ф₀))'
