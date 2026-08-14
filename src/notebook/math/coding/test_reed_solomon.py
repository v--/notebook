from collections.abc import Sequence

from notebook.math.rings.modular import Z5
from notebook.support.pytest import pytest_parametrize_kwargs

from .reed_solomon import naive_reed_solomon_decode, reed_solomon_encode


@pytest_parametrize_kwargs(
    dict(field=Z5, message=[3], points=[3, 4], expected=[3, 3]),
    dict(field=Z5, message=[0, 1, 2], points=[0, 1, 2, 3, 4], expected=[0, 3, 0, 1, 1]),
)
def test_reed_solomon_encode(field: type, message: Sequence[int], points: Sequence[int], expected: Sequence[int]) -> None:
    string_ = [field(n) for n in message]
    points_ = [field(n) for n in points]
    expected_ = [field(n) for n in expected]

    encoded = reed_solomon_encode(string_, points_)
    assert encoded == expected_


@pytest_parametrize_kwargs(
    # We start with the real codeword and replace a digit
    dict(field=Z5, codeword=[3, 3], expected=[3]),
    dict(field=Z5, codeword=[3, 4], expected=[3]),
    dict(field=Z5, codeword=[4, 3], expected=[3]),

    # We start with the real codeword and replace up to 2 digits
    dict(field=Z5, codeword=[0, 3, 0, 1, 1], expected=[0, 1, 2]),
    dict(field=Z5, codeword=[4, 3, 0, 1, 1], expected=[0, 1, 2]),
    dict(field=Z5, codeword=[4, 4, 0, 1, 1], expected=[0, 1, 2]),
)
def test_naive_reed_solomon_decode(field: type, codeword: Sequence[int], expected: Sequence[int]) -> None:
    codeword_ = [field(n) for n in codeword]
    expected_ = [field(n) for n in expected]

    decoded = naive_reed_solomon_decode(codeword_, len(expected_))
    assert decoded == expected_
