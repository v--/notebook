import pytest

from notebook.math.rings.modular import Z2
from notebook.support.pytest import pytest_parametrize_kwargs

from .exceptions import DecodingError
from .parity_check import parity_check_decode, parity_check_encode


@pytest_parametrize_kwargs(
    dict(message='0'),
    dict(message='1'),
    dict(message='01'),
    dict(message='1101'),
)
def test_parity_check_encode(message: str) -> None:
    string_ = [Z2(int(n)) for n in message]
    encoded = parity_check_encode(string_)
    decoded = parity_check_decode(encoded)
    assert decoded == string_


@pytest_parametrize_kwargs(
    dict(codeword='0'),
    dict(codeword='01'),
    dict(codeword='111'),
)
def test_parity_check_decode_invalid(codeword: str) -> None:
    string_ = [Z2(int(n)) for n in codeword]

    with pytest.raises(DecodingError):
        parity_check_decode(string_)
