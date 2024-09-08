from .unicode import (
    Capitalization,
    atoi_subscripts,
    is_greek_string,
    is_latin_string,
    itoa_subscripts,
    normalize_whitespace,
    remove_accents,
    to_superscript,
)


def test_to_superscript() -> None:
    assert to_superscript('abc') == 'ᵃᵇᶜ'
    assert to_superscript('ABC') == 'ᴬᴮꟲ'
    assert to_superscript('AbC') == 'ᴬᵇꟲ'
    assert to_superscript('абв') == 'абв'


def test_atoi_subscripts() -> None:
    assert atoi_subscripts('₀') == 0
    assert atoi_subscripts('₁₂₃₄') == 1234
    assert atoi_subscripts('₋₁₂₃₄') == -1234


def test_itoa_subscripts() -> None:
    assert itoa_subscripts(0) == '₀'
    assert itoa_subscripts(-1234) == '₋₁₂₃₄'
    assert itoa_subscripts(1234) == '₁₂₃₄'


def test_is_latin_string() -> None:
    assert is_latin_string('abc', capitalization=Capitalization.mixed)
    assert is_latin_string('ABC', capitalization=Capitalization.mixed)
    assert is_latin_string('AbC', capitalization=Capitalization.mixed)

    assert is_latin_string('abc', capitalization=Capitalization.small)
    assert not is_latin_string('ABC', capitalization=Capitalization.small)
    assert not is_latin_string('AbC', capitalization=Capitalization.small)

    assert not is_latin_string('abc', capitalization=Capitalization.capital)
    assert is_latin_string('ABC', capitalization=Capitalization.capital)
    assert not is_latin_string('AbC', capitalization=Capitalization.capital)


def test_is_greek_string() -> None:
    assert is_greek_string('αβγ', capitalization=Capitalization.mixed)
    assert is_greek_string('ΑΒΓ', capitalization=Capitalization.mixed)
    assert is_greek_string('ΑβΓ', capitalization=Capitalization.mixed)

    assert is_greek_string('αβγ', capitalization=Capitalization.small)
    assert not is_greek_string('ΑΒΓ', capitalization=Capitalization.small)
    assert not is_greek_string('ΑβΓ', capitalization=Capitalization.small)

    assert not is_greek_string('αβγ', capitalization=Capitalization.capital)
    assert is_greek_string('ΑΒΓ', capitalization=Capitalization.capital)
    assert not is_greek_string('ΑβΓ', capitalization=Capitalization.capital)


def test_remove_accents() -> None:
    assert remove_accents('lorem') == 'lorem'
    assert remove_accents('Йордан') == 'Йордан'

    assert remove_accents('Fučík') == 'Fucik'
    assert remove_accents('Marián') == 'Marian'
    assert remove_accents('Łukasz') == 'Lukasz'


def test_normalize_whitespace() -> None:
    assert normalize_whitespace('a b c') == 'a b c'
    assert normalize_whitespace('a  b c') == 'a b c'
    assert normalize_whitespace('a\tb c') == 'a b c'
    assert normalize_whitespace('a\nb c') == 'a b c'
