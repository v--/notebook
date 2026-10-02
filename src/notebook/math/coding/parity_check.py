import functools
import operator
lazy from collections.abc import Sequence

from notebook.support.coderefs import collector
lazy from notebook.math.rings.modular import Z2

from .exceptions import DecodingError, EncodingError


@collector.ref('alg:parity_check_code')
def parity_check_encode(message: Sequence[Z2]) -> Sequence[Z2]:
    if len(message) == 0:
        raise EncodingError('Cannot encode the empty message')

    return [*message, functools.reduce(operator.add, message)]


def parity_check_decode(codeword: Sequence[Z2]) -> Sequence[Z2]:
    if len(codeword) < 2:
        raise DecodingError(f'Codeword {codeword} is too short')

    *message, check_bit = codeword

    if check_bit != functools.reduce(operator.add, message):
        raise DecodingError(f'Invalid parity check bit for codeword {codeword}')

    return message
