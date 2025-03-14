from .alphabets import Capitalization, is_greek_string, is_latin_string


def xnor(a: bool, b: bool) -> bool:  # noqa: FBT001
    return a == b


def test_is_latin_string_capitaliation(string: str = 'abc') -> None:
    lower = string.lower()
    upper = string.upper()
    mixed = string.title()

    for cap in Capitalization:
        assert xnor(Capitalization.LOWER in cap, is_latin_string(lower, capitalization=cap))
        assert xnor(Capitalization.UPPER in cap, is_latin_string(upper, capitalization=cap))
        assert xnor(Capitalization.MIXED in cap, is_latin_string(mixed, capitalization=cap))


def test_is_greek_string_capitaliation(string: str = 'τσρ') -> None:
    lower = string.lower()
    upper = string.upper()
    mixed = string.title()

    for cap in Capitalization:
        assert xnor(Capitalization.LOWER in cap, is_greek_string(lower, capitalization=cap))
        assert xnor(Capitalization.UPPER in cap, is_greek_string(upper, capitalization=cap))
        assert xnor(Capitalization.MIXED in cap, is_greek_string(mixed, capitalization=cap))
