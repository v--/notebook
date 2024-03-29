from typing import Iterable


def atoi_subscripts(string: str) -> int:
    if string[0] == '₋':
        return -atoi_subscripts(string[1:])

    return sum(
        (ord(digit) - ord('₀')) * (10 ** i)
        for i, digit in enumerate(reversed(string))
    )


def _iter_itoa_subscripts(value: int) -> Iterable[str]:
    assert value > 0

    while value > 0:
        yield chr(ord('₀') + value % 10)

        if value == 10:
            yield '₀'

        value //= 10


def itoa_subscripts(value: int) -> str:
    if value == 0:
        return '₀'

    if value < 0:
        return '₋' + itoa_subscripts(-value)

    return ''.join(reversed(list(_iter_itoa_subscripts(value))))
