from collections.abc import Mapping

from notebook.math.rings.modular import Z5, IntModuloMeta, BaseIntModulo
from notebook.support.pytest import pytest_parametrize_kwargs

from .reed_solomon import naive_reed_solomon_list_decode, reed_solomon_encode


@pytest_parametrize_kwargs(
    dict(field=Z5, message='3', points='34', expected='33'),
    dict(field=Z5, message='012', points='01234', expected='03011'),
)
def test_reed_solomon_encode(field: type, message: str, points: str, expected: str) -> None:
    string_ = [field(int(n)) for n in message]
    points_ = [field(int(n)) for n in points]
    expected_ = [field(int(n)) for n in expected]

    encoded = reed_solomon_encode(string_, points_)
    assert encoded == expected_


@pytest_parametrize_kwargs(
    # The correct code of '3' is '33'; changing one digit introduces other viable candidates
    dict(field=Z5, codeword='33', expected={'3'}),
    dict(field=Z5, codeword='34', expected={'3', '4'}),
    dict(field=Z5, codeword='43', expected={'3', '4'}),

    # The correct code of '012' is '03011'; changing one digit is safe, but two digits introduce other candidates
    dict(field=Z5, codeword='03011', expected={'012'}),
    dict(field=Z5, codeword='43011', expected={'012'}),
    dict(field=Z5, codeword='04011', expected={'012'}),
    dict(field=Z5, codeword='44011', expected={'012', '144', '243', '310', '411', '423', '424', '430', '432', '441'}),
)
def test_naive_reed_solomon_list_decode(field: IntModuloMeta, codeword: str, expected: Mapping[str, float]) -> None:
    codeword_ = [field(int(n)) for n in codeword]
    message_length = len(next(iter(expected)))
    decoded_iter = naive_reed_solomon_list_decode(codeword=codeword_, message_length=message_length)
    decoded_as_set = {''.join(str(n.value) for n in message) for message in decoded_iter}
    assert decoded_as_set == expected
