from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue

from ...exceptions import BibToolsParsingError


def create_lang_object(language: str) -> Lang:
    try:
        if len(language) == 2:
            return Lang(language)

        return Lang(language.title())
    except InvalidLanguageValue as err:
        raise BibToolsParsingError(f'Unrecognized language {language!r}') from err


def get_language_name(language: str) -> str:
    return create_lang_object(language).name.lower()


normalize_language_name = get_language_name


def get_language_code(language: str) -> str:
    return create_lang_object(language).pt1
