from .subscripts import atoi_subscripts, itoa_subscripts


def test_atoi_subscripts():
    assert atoi_subscripts('₀') == 0
    assert atoi_subscripts('₁₂₃₄') == 1234
    assert atoi_subscripts('₋₁₂₃₄') == -1234


def test_itoa_subscripts():
    assert itoa_subscripts(0) == '₀'
    assert itoa_subscripts(-1234) == '₋₁₂₃₄'
    assert itoa_subscripts(1234) == '₁₂₃₄'
