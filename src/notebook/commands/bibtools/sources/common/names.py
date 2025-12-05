from nameparser import HumanName

from .....bibtex import BibAuthor, BibString, parse_value


def normalize_human_name(full_name: BibString) -> BibString:
    if isinstance(full_name, str):
        return str(HumanName(full_name))

    return full_name


def is_name_normalized(full_name: BibString) -> bool:
    return normalize_human_name(full_name) == full_name


def get_main_human_name(full_name: BibString) -> BibString:
    if isinstance(full_name, str):
        names = HumanName(full_name)
        return names.last or names.first

    return full_name


def name_to_bib_author(full_name: BibString) -> BibAuthor:
    if isinstance(full_name, str):
        return BibAuthor(full_name=parse_value(full_name))

    return BibAuthor(full_name=full_name)
