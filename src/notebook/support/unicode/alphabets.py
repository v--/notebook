from enum import Flag, auto


class Capitalization(Flag):
    SMALL = auto()
    CAPITAL = auto()
    ANY = CAPITAL | SMALL


def is_latin_string(string: str, capitalization: Capitalization) -> bool:
    return all(
        ('A' <= c <= 'Z' if Capitalization.CAPITAL in capitalization else False) or
        ('a' <= c <= 'z' if Capitalization.SMALL in capitalization else False)
        for c in string
    )


def is_greek_string(string: str, capitalization: Capitalization) -> bool:
    return all(
        ('Α' <= c <= 'Ω' if Capitalization.CAPITAL in capitalization else False) or
        ('α' <= c <= 'ω' if Capitalization.SMALL in capitalization else False)
        for c in string
    )
