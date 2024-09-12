from nameparser import HumanName

from notebook.bibtex.author import BibAuthor


def name_to_bib_author(full_name: str) -> BibAuthor:
    names = HumanName(full_name)

    if names.last == '':
        return BibAuthor(
            main_name=names.first,
            title=None,
            other_names=None
        )

    return BibAuthor(
        main_name=names.last,
        title=names.title or None,
        other_names=' '.join(filter(bool, [names.first, names.middle, names.suffix]))
    )