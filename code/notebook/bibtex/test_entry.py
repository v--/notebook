from textwrap import dedent

from .author import BibAuthor
from .entry import BibEntry
from .string import CompositeString, VerbatimString


def test_entry_stringify() -> None:
    entry = BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(full_name='A B'), BibAuthor(full_name='C D')],
        languages=['english']
    )

    assert str(entry) == dedent(r'''
        @book{test,
          author = {A B and C D},
          language = {english},
          title = {Test}
        }
        '''[1:])


def test_entry_stringify_multilang() -> None:
    entry = BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(full_name='A B')],
        languages=['english', 'russian']
    )

    assert str(entry) == dedent(r'''
        @book{test,
          author = {A B},
          language = {english and russian},
          title = {Test}
        }
        '''[1:])


def test_entry_stringify_verbatim_author() -> None:
    entry = BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(full_name=VerbatimString('A B'))],
        languages=['english']
    )

    assert str(entry) == dedent(r'''
        @book{test,
          author = {{A B}},
          language = {english},
          title = {Test}
        }
        '''[1:])


def test_entry_stringify_partially_verbatim_author() -> None:
    entry = BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(full_name=CompositeString(['The ', VerbatimString('A B')]))],
        languages=['english']
    )

    assert str(entry) == dedent(r'''
        @book{test,
          author = {The {A B}},
          language = {english},
          title = {Test}
        }
        '''[1:])


def test_entry_stringify_shortauthor() -> None:
    entry = BibEntry(
        entry_type='book',
        entry_name='тест',
        title='Тест',
        authors=[BibAuthor(full_name='А', short_name='A'), BibAuthor(full_name='Б', short_name='B')],
        languages=['russian']
    )

    assert str(entry) == dedent(r'''
        @book{тест,
          author = {А and Б},
          language = {russian},
          shortauthor = {A and B},
          title = {Тест}
        }
        '''[1:])

