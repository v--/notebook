from ...support.unicode import Capitalization, is_greek_string, is_latin_string, is_numeric_subscript_char


def is_latin_identifier(string: str, capitalization: Capitalization) -> bool:
    if len(string) == 0:
        return False

    return is_latin_string(string[0], capitalization) and all(is_numeric_subscript_char(c) for c in string[1:])


def is_greek_identifier(string: str, capitalization: Capitalization) -> bool:
    if len(string) == 0:
        return False

    return is_greek_string(string[0], capitalization) and all(is_numeric_subscript_char(c) for c in string[1:])
