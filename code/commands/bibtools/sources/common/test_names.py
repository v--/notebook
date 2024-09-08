import pytest

from notebook.bibtex.author import BibAuthor

from .names import name_to_bib_author


@pytest.mark.parametrize(
    'bib_author',
    [
        BibAuthor(main_name='Колмогоров', other_names='Андрей Николаевич'),
        BibAuthor(main_name='Магарил-Ильяев', other_names='Георгий Георгиевич'),
        BibAuthor(main_name='Mac Lane', other_names='Saunders'),
        BibAuthor(main_name='von Plato', other_names='Jan')
    ]
)
def test_name_to_bib_author(bib_author: BibAuthor) -> None:
    assert name_to_bib_author(f'{bib_author.main_name}, {bib_author.other_names}') == bib_author
    assert name_to_bib_author(f'{bib_author.other_names} {bib_author.main_name}') == bib_author


def test_name_to_bib_author_euclid() -> None:
    assert name_to_bib_author('Euclid of Alexandria') == BibAuthor(main_name='Euclid of Alexandria')
