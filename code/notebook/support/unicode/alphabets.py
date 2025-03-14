from enum import Flag, auto


class Capitalization(Flag):
    LOWER = auto()
    UPPER = auto()
    MIXED = UPPER | LOWER


def is_latin_string(string: str, capitalization: Capitalization) -> bool:
    return all(
        ('A' <= c <= 'Z' if Capitalization.UPPER in capitalization else False) or
        ('a' <= c <= 'z' if Capitalization.LOWER in capitalization else False)
        for c in string
    )


def is_greek_string(string: str, capitalization: Capitalization) -> bool:
    return all(
        ('Α' <= c <= 'Ω' if Capitalization.UPPER in capitalization else False) or
        ('α' <= c <= 'ω' if Capitalization.LOWER in capitalization else False)
        for c in string
    )
