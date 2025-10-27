from nameparser import HumanName

from .....bibtex.author import BibAuthor
from .....bibtex.parsing import parse_value
from .....bibtex.string import BibString


def normalize_human_name(full_name: BibString) -> BibString:
    if isinstance(full_name, str):
        return str(HumanName(full_name))

    return full_name


def get_main_human_name(full_name: BibString) -> BibString:
    if isinstance(full_name, str):
        names = HumanName(full_name)
        return names.last or names.first

    return full_name


def name_to_bib_author(full_name: BibString) -> BibAuthor:
    if isinstance(full_name, str):
        return BibAuthor(full_name=parse_value(full_name))

    return BibAuthor(full_name=full_name)
