from .unicode import atoi_subscripts, itoa_subscripts, to_superscript


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
