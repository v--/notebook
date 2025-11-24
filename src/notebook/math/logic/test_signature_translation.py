import pytest

from .parsing import parse_formula, parse_term
from .signature import FormalLogicSignature
from .signature_translation import SignatureTranslation, SignatureTranslationError, translate_formula, translate_term


def test_translation_kind_mismatch(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(SignatureTranslationError, match="Mismatch between the function symbol 'f¹' and the predicate symbol 'p¹'"):
        SignatureTranslation({ dummy_signature.get_symbol('f¹'): dummy_signature.get_symbol('p¹') })


def test_translation_arity_mismatch(dummy_signature: FormalLogicSignature) -> None:
    with pytest.raises(SignatureTranslationError, match="Mismatch between 'f¹' of arity 1 and 'g²' of arity 2"):
        SignatureTranslation({ dummy_signature.get_symbol('f¹'): dummy_signature.get_symbol('g²') })


def test_translate_term(dummy_signature: FormalLogicSignature) -> None:
    target_signature = FormalLogicSignature()
    target_signature.add_symbol('FUNCTION', 'ф²', 2, infix=False)
    target_signature.add_symbol('FUNCTION', 'г¹', 1, infix=False)

    translation = SignatureTranslation({
        dummy_signature.get_symbol('f²'): target_signature.get_symbol('ф²'),
        dummy_signature.get_symbol('g¹'): target_signature.get_symbol('г¹')
    })

    term = parse_term('f²(g¹(x), y)', dummy_signature)
    assert str(translate_term(translation, term)) == 'ф²(г¹(x), y)'


def test_translate_term_exchange_prefix_and_infix(dummy_signature: FormalLogicSignature) -> None:
    translation = SignatureTranslation({
        dummy_signature.get_symbol('f²'): dummy_signature.get_symbol('+'),
        dummy_signature.get_symbol('×'): dummy_signature.get_symbol('g²'),
    })

    term = parse_term('f²(x, (y × z))', dummy_signature)
    assert str(translate_term(translation, term)) == '(x + g²(y, z))'


def test_translate_formula(dummy_signature: FormalLogicSignature) -> None:
    target_signature = FormalLogicSignature()
    target_signature.add_symbol('FUNCTION', 'ф⁰', 0, infix=False)
    target_signature.add_symbol('PREDICATE', 'п¹', 1, infix=False)

    translation = SignatureTranslation({
        dummy_signature.get_symbol('f⁰'): target_signature.get_symbol('ф⁰'),
        dummy_signature.get_symbol('p¹'): target_signature.get_symbol('п¹')
    })

    formula = parse_formula('¬∃x.(p¹(x) → p¹(f⁰))', dummy_signature)
    assert str(translate_formula(translation, formula)) == '¬∃x.(п¹(x) → п¹(ф⁰))'
