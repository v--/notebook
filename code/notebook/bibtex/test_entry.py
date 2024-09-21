from textwrap import dedent

from .author import BibAuthor
from .entry import BibEntry


def test_entry_stringify() -> None:
    entry = BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='A', other_names='B'), BibAuthor(main_name='C', other_names='D')],
        language='english'
    )

    assert str(entry) == dedent(r'''
        @book{test,
          author = {A, B and C, D},
          language = {english},
          title = {Test}
        }
        '''[:-1])


def test_entry_stringify_literal_author() -> None:
    entry = BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='{A B}', verbatim=True)],
        language='english'
    )

    assert str(entry) == dedent(r'''
        @book{test,
          author = {{A B}},
          language = {english},
          title = {Test}
        }
        '''[:-1])

def test_entry_stringify_shortauthor() -> None:
    entry = BibEntry(
        entry_type='book',
        entry_name='тест',
        title='Тест',
        authors=[BibAuthor(main_name='А', display_name='A'), BibAuthor(main_name='Б', display_name='B')],
        language='russian'
    )

    assert str(entry) == dedent(r'''
        @book{тест,
          author = {А and Б},
          language = {russian},
          shortauthor = {A and B},
          title = {Тест}
        }
        '''[:-1])
