from nameparser import HumanName

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.verbatim import is_verbatim_string


def normalize_human_name(full_name: str) -> str:
    return str(HumanName(full_name))


def normalize_author_name(author: BibAuthor) -> str:
    if author.verbatim:
        return author.full_name

    return normalize_human_name(author.full_name)


def get_main_human_name(full_name: str) -> str:
    names = HumanName(full_name)
    return names.last or names.first


def get_main_author_name(author: BibAuthor) -> str:
    if author.verbatim:
        return author.full_name

    return get_main_human_name(author.full_name)


def name_to_bib_author(full_name: str) -> BibAuthor:
    if is_verbatim_string(full_name):
        return BibAuthor(full_name=full_name, verbatim=True)

    return BibAuthor(full_name=full_name, verbatim=False)
