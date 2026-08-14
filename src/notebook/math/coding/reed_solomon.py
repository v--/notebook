import functools
import itertools
import operator
from collections.abc import Sequence

from notebook.math.lang.distance import hamming_distance
from notebook.math.rings.modular import BaseIntModulo
from notebook.support.coderefs import collector

from .exceptions import DecodingError, EncodingError


@collector.ref('alg:reed_solomon_code')
def reed_solomon_encode[T: BaseIntModulo](message: Sequence[T], points: Sequence[T]) -> Sequence[T]:
    if len(message) == 0:
        raise EncodingError('Cannot encode the empty message')

    if len(message) > len(points):
        raise EncodingError('Must provide more points than the length of the message')

    if len(set(points)) < len(points):
        raise EncodingError('The points must be unique')

    return [
        functools.reduce(operator.add, (digit * p ** k for k, digit in enumerate(message)))
        for p in points
    ]


def naive_reed_solomon_decode[T: BaseIntModulo](codeword: Sequence[T], message_length: int) -> Sequence[T]:
    if len(codeword) < 1:
        raise DecodingError('Codeword cannot be empty')

    if message_length >= len(codeword):
        raise EncodingError('The message length must be less than that of the codeword')

    first = codeword[0]

    for message in itertools.product(map(first.new, range(first.modulus)), repeat=message_length):
        for points in itertools.combinations(map(first.new, range(first.modulus)), len(codeword)):
            if hamming_distance(codeword, reed_solomon_encode(message, points)) <= len(codeword) - message_length:
                return list(message)

    raise DecodingError(f'Cannot decode codeword {codeword}')
