
from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue

from notebook.bibtex.entry import BibEntry
from notebook.bibtex.string import BibString, strip_braces

from ...exceptions import BibToolsParsingError


def create_lang_object(language: str) -> Lang:
    try:
        if len(language) == 2:
            return Lang(language)

        return Lang(language.title())
    except InvalidLanguageValue as err:
        raise BibToolsParsingError(f'Unrecognized language {language!r}') from err


def get_language_name(language: BibString) -> BibString:
    if isinstance(language, str):
        return create_lang_object(language).name.lower()

    return language


normalize_language_name = get_language_name


def get_language_code(language: BibString) -> BibString:
    if isinstance(language, str):
        return create_lang_object(language).pt1

    return language


def get_main_entry_language(entry: BibEntry) -> str:
    if len(entry.languages) == 0:
        return 'english'

    return strip_braces(entry.languages[0])
