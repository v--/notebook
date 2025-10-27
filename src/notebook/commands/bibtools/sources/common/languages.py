from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue

from .....bibtex.entry import BibEntry
from .....bibtex.string import BibString, strip_braces
from ...exceptions import BibToolsParsingError


def create_lang_object(language: str) -> Lang:
    try:
        if len(language) == 2:
            return Lang(language)

        return Lang(language.title())
    except InvalidLanguageValue as err:
        raise BibToolsParsingError(f'Unrecognized language {language!r}') from err


def get_language_name(language: BibString) -> str:
    # We handle greek specially because iso639 and biblatex have differing opinions on handling it
    if isinstance(language, str) and language.strip().lower() == 'greek':
        return 'greek'

    if isinstance(language, str):
        return create_lang_object(language).name.lower()

    return strip_braces(language)


normalize_language_name = get_language_name


def get_language_code(language: BibString) -> BibString:
    normalized = get_language_name(language)

    if normalized == 'greek':
        # In iso639, grc is ancient Greek, gre is modern Greek
        # Ancient greek does not have two-letter code
        return 'el'

    return create_lang_object(normalized).pt1


def get_main_entry_language(entry: BibEntry) -> str:
    if len(entry.languages) == 0:
        return 'english'

    return normalize_language_name(entry.languages[0])
