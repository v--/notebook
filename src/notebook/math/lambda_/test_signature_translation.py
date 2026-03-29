from .algebraic_types import SIMPLE_ALGEBRAIC_SIGNATURE
from .parsing import parse_type, parse_typed_term
from .signature import SignatureMorphism
from .signature_translation import translate_term, translate_type


def test_translate_type() -> None:
    translation = SignatureMorphism(SIMPLE_ALGEBRAIC_SIGNATURE, {
        SIMPLE_ALGEBRAIC_SIGNATURE['𝟘']: SIMPLE_ALGEBRAIC_SIGNATURE['𝟙'],
        SIMPLE_ALGEBRAIC_SIGNATURE['𝟙']: SIMPLE_ALGEBRAIC_SIGNATURE['𝟘'],
    })

    type_ = parse_type('(τ → (𝟘 × 𝟙))', SIMPLE_ALGEBRAIC_SIGNATURE)
    assert str(translate_type(translation, type_)) == '(τ → (𝟙 × 𝟘))'


def test_translate_formula() -> None:
    translation = SignatureMorphism(SIMPLE_ALGEBRAIC_SIGNATURE, {
        SIMPLE_ALGEBRAIC_SIGNATURE['𝟘']: SIMPLE_ALGEBRAIC_SIGNATURE['𝟙'],
        SIMPLE_ALGEBRAIC_SIGNATURE['𝟙']: SIMPLE_ALGEBRAIC_SIGNATURE['𝟘'],
        SIMPLE_ALGEBRAIC_SIGNATURE['S₊ₗ']: SIMPLE_ALGEBRAIC_SIGNATURE['S₊ᵣ'],
        SIMPLE_ALGEBRAIC_SIGNATURE['S₊ᵣ']: SIMPLE_ALGEBRAIC_SIGNATURE['S₊ₗ'],
    })

    term = parse_typed_term('(λx:𝟘.(S₊ₗx))', SIMPLE_ALGEBRAIC_SIGNATURE)
    assert str(translate_term(translation, term)) == '(λx:𝟙.(S₊ᵣx))'
