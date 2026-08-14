import functools
import itertools
import operator
lazy from collections.abc import Iterable, Sequence

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


def iter_reed_solomon_matches[T: BaseIntModulo](codeword: Sequence[T], message_length: int) -> Iterable[tuple[Sequence[T], int]]:
    max_distance = len(codeword) - message_length
    cls = type(codeword[0])

    for message in itertools.product(map(cls, range(cls.modulus)), repeat=message_length):
        for points in itertools.combinations(map(cls, range(cls.modulus)), len(codeword)):
            distance = hamming_distance(codeword, reed_solomon_encode(message, points))

            if distance <= max_distance:
                yield list(message), distance
                break


def naive_reed_solomon_list_decode[T: BaseIntModulo](codeword: Sequence[T], message_length: int) -> Iterable[Sequence[T]]:
    if len(codeword) < 1:
        raise DecodingError('Codeword cannot be empty')

    if message_length >= len(codeword):
        raise EncodingError('The message length must be less than that of the codeword')

    min_dist: int | None = None

    for message, dist in sorted(
        iter_reed_solomon_matches(codeword, message_length),
        key=operator.itemgetter(1),
    ):
        if min_dist is None:
            min_dist = dist
        elif dist > min_dist:
            break

        yield message
