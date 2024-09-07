from textwrap import dedent

import pytest

from ...parsing.parser import ParsingError
from ..entry import BibAuthor, BibEntry
from .parser import parse_bibtex


def test_comment() -> None:
    assert parse_bibtex('% test') == []


def test_empty_lines() -> None:
    assert parse_bibtex('\n\t% test\n') == []


def test_invalid_entry() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(' test')

    assert str(excinfo.value) == 'A bibtex entry must start with @'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │  test
          │  ^^^^
        '''[1:]
    )


def test_invalid_entry_type() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex('@123\n')

    assert str(excinfo.value) == 'Expected an entry type'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @123↵
          │  ^^^
        '''[1:]
    )


def test_end_after_entry_type() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex('@book')

    assert str(excinfo.value) == 'An opening brace must follow a bibtex entry type'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book
          │  ^^^^
        '''[1:]
    )


def test_unknown_entry_type() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex('@test')

    assert str(excinfo.value) == 'Unrecognized entry type'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @test
          │  ^^^^
        '''[1:]
    )


def test_invalid_entry_name() -> None:
    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex('@book{')

    assert str(excinfo.value) == 'Expected an entry name'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{
          │      ^
        '''[1:]
    )


def test_no_properties() -> None:
    string = dedent(r'''
        @book{test}
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Entry without properties'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test}↵
          │ ^^^^^^^^^^^
      '''[1:]
    )


def test_no_title() -> None:
    string = dedent(r'''
        @book{test,
          edition = 1
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Entry without title'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
          │ ^^^^^^^^^^^^
        2 │   edition = 1↵
          │ ^^^^^^^^^^^^^^
        3 │ }↵
          │ ^
      '''[1:]
    )


def test_no_authors() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Entry without authors'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
          │ ^^^^^^^^^^^^
        2 │   title = {Test}↵
          │ ^^^^^^^^^^^^^^^^^
        3 │ }↵
          │ ^
      '''[1:]
    )


def test_no_language() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Entry without language'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
          │ ^^^^^^^^^^^^
        2 │   title = {Test},↵
          │ ^^^^^^^^^^^^^^^^^^
        3 │   author = {A, B}↵
          │ ^^^^^^^^^^^^^^^^^^
        4 │ }↵
          │ ^
      '''[1:]
    )


def test_invalid_language() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {engrish}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Unrecognized language'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test},↵
        3 │   author = {A, B},↵
        4 │   language = {engrish}↵
          │              ^^^^^^^^^
      '''[1:]
    )


def test_minimal_valid_entry() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {english}
        }
        '''[1:]
    )
    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='A', other_names='B')],
        language='english'
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='A', other_names='B')],
        language='english'
    )


def test_trailing_comma() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {english},
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Trailing commas are disallowed'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test},↵
        3 │   author = {A, B},↵
        4 │   language = {english},↵
          │                       ^
      '''[1:]
    )


def test_author_with_and_in_name() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {Randy},
          language = {english}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='Randy')],
        language='english'
    )


def test_multiple_authors() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B and C, D},
          language = {english}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='A', other_names='B'), BibAuthor(main_name='C', other_names='D')],
        language='english'
    )

def test_translator() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          translator = {C, D},
          language = {english}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='A', other_names='B')],
        translators=[BibAuthor(main_name='C', other_names='D')],
        language='english'
    )


def test_authors_only_and() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {and},
          language = {english}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Cannot parse author string'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test},↵
        3 │   author = {and},↵
          │            ^^^^^
      '''[1:]
    )


def test_authors_double_and() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A and and B},
          language = {english}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Cannot parse author string'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test},↵
        3 │   author = {A and and B},↵
          │            ^^^^^^^^^^^^^
      '''[1:]
    )


def test_authors_empty_name() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A,},
          language = {english}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Cannot parse author string'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test},↵
        3 │   author = {A,},↵
          │            ^^^^
      '''[1:]
    )


def test_single_verbatim_author() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {{Verbatim}},
          language = {english}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='{Verbatim}')],
        language='english'
    )


def test_multiple_verbatim_authors() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {{Verbatim} and {Verbatim 2}},
          language = {english}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='{Verbatim}'), BibAuthor(main_name='{Verbatim 2}')],
        language='english'
    )


def test_mixed_verbatim_author() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, {B and C, D}},
          language = {english}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Cannot parse author string'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test},↵
        3 │   author = {A, {B and C, D}},↵
          │            ^^^^^^^^^^^^^^^^^
      '''[1:]
    )


def test_one_verbatim_authors_with_and() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {{Verbatim and Verbatim 2}},
          language = {english}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='{Verbatim and Verbatim 2}')],
        language='english'
    )


def test_one_verbatim_authors_with_and_quotes() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = "{Verbatim and Verbatim 2}",
          language = {english}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='{Verbatim and Verbatim 2}')],
        language='english'
    )


def test_minimal_valid_entry_escape() -> None:
    string = dedent(r'''
        @book{test,
          title = {\{Test\}},
          author = {A, B},
          language = {english}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='{Test}',
        authors=[BibAuthor(main_name='A', other_names='B')],
        language='english'
    )


def test_minimal_valid_entry_quotes() -> None:
    string = dedent(r'''
        @book{test,
          title = "Test",
          author = "A, B",
          language = "english"
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='A', other_names='B')],
        language='english'
    )


def test_minimal_valid_entry_quote_escape() -> None:
    string = dedent(r'''
        @book{test,
          title = "Test {"}",
          author = "A, B",
          language = "english"
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test "',
        authors=[BibAuthor(main_name='A', other_names='B')],
        language='english'
    )


def test_unclosed_demimiter() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test'''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Unclosed delimiter'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test
          │           ^^^^^
      '''[1:]
    )


def test_escape_truncated() -> None:
    string = dedent('''
        @book{test,
          title = {Test \\'''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Invalid escaped symbol'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test \
          │                 ^
      '''[1:]
    )


def test_invalid_escape() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test \},
          author = {A, B},
          language = {english}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Unexpected line break'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test \},↵
          │                    ^
      '''[1:]
    )


def test_two_valid_entries() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {english}
        }

        @book{тест,
          title = {Тест},
          author = {А, Б},
          language = {russian}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 2
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(other_names='B', main_name='A')],
        language='english'
    )
    assert entries[1] == BibEntry(
        entry_type='book',
        entry_name='тест',
        title='Тест',
        authors=[BibAuthor(main_name='А', other_names='Б')],
        language='russian'
    )


def test_duplicate_name() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {english}
        }

        @book{test,
          title = {Test},
          author = {A, B},
          language = {english}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Duplicate entry name'
    assert excinfo.value.__notes__[0] == dedent(r'''
        7 │ @book{test,↵
          │       ^^^^
      '''[1:]
    )


def test_ampersand_removal() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {english},
          publisher = {Chapman \& Hall/CRC}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='A', other_names='B')],
        language='english',
        publisher='Chapman & Hall/CRC'
    )


def test_url_ampersand_removal() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {english},
          url = {http://api.com?a=1&b=2}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='test',
        title='Test',
        authors=[BibAuthor(main_name='A', other_names='B')],
        language='english',
        url='http://api.com?a=1&b=2'
    )


def test_empty_isbn() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {english},
          isbn = {}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Empty value'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test},↵
        3 │   author = {A, B},↵
        4 │   language = {english},↵
        5 │   isbn = {}↵
          │          ^^
      '''[1:]
    )


def test_invalid_isbn() -> None:
    string = dedent(r'''
        @book{test,
          title = {Test},
          author = {A, B},
          language = {english},
          isbn = {000}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == 'Invalid ISBN'
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{test,↵
        2 │   title = {Test},↵
        3 │   author = {A, B},↵
        4 │   language = {english},↵
        5 │   isbn = {000}↵
          │          ^^^^^
      '''[1:]
    )


def test_shortauthor_simple() -> None:
    string = dedent(r'''
        @book{тест,
          title = {Тест},
          author = {А, Б},
          shortauthor = {A},
          language = {russian}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='тест',
        title='Тест',
        authors=[BibAuthor(main_name='А', other_names='Б', display_name='A')],
        language='russian'
    )


def test_shortauthor_two_names() -> None:
    string = dedent(r'''
        @book{тест,
          title = {Тест},
          author = {А, Б and В, Г},
          shortauthor = {A and V},
          language = {russian}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='book',
        entry_name='тест',
        title='Тест',
        authors=[
            BibAuthor(main_name='А', other_names='Б', display_name='A'),
            BibAuthor(main_name='В', other_names='Г', display_name='V')
        ],
        language='russian'
    )


def test_shortauthor_insufficient() -> None:
    string = dedent(r'''
        @book{тест,
          title = {Тест},
          author = {А, Б and В, Г},
          shortauthor = {A},
          language = {russian}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == "Property 'shortauthor' does not match the structure of 'author'"
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{тест,↵
          │ ^^^^^^^^^^^^
        2 │   title = {Тест},↵
          │ ^^^^^^^^^^^^^^^^^^
        3 │   author = {А, Б and В, Г},↵
          │ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        4 │   shortauthor = {A},↵
          │ ^^^^^^^^^^^^^^^^^^^^^
        5 │   language = {russian}↵
          │ ^^^^^^^^^^^^^^^^^^^^^^^
        6 │ }↵
          │ ^
      '''[1:]
    )


def test_shortauthor_verbatim_overfull() -> None:
    string = dedent(r'''
        @book{тест,
          title = {Тест},
          author = {А, Б},
          shortauthor = {A and V},
          language = {russian}
        }
        '''[1:]
    )

    with pytest.raises(ParsingError) as excinfo:
        parse_bibtex(string)

    assert str(excinfo.value) == "Property 'shortauthor' does not match the structure of 'author'"
    assert excinfo.value.__notes__[0] == dedent(r'''
        1 │ @book{тест,↵
          │ ^^^^^^^^^^^^
        2 │   title = {Тест},↵
          │ ^^^^^^^^^^^^^^^^^^
        3 │   author = {А, Б},↵
          │ ^^^^^^^^^^^^^^^^^^^
        4 │   shortauthor = {A and V},↵
          │ ^^^^^^^^^^^^^^^^^^^^^^^^^^^
        5 │   language = {russian}↵
          │ ^^^^^^^^^^^^^^^^^^^^^^^
        6 │ }↵
          │ ^
      '''[1:]
    )


def test_article_entry() -> None:
    string = dedent(r'''
        @article{Blass1984AOC,
          author = {Blass, Andreas},
          journal = {Contemporary Mathematics},
          language = {english},
          publisher = {American Mathematical Society (AMS)},
          title = {Existence of Bases Implies the Axiom of Choice},
          url = {http://www.math.lsa.umich.edu/ ablass/bases-AC.pdf},
          volume = {31},
          year = {1984}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='article',
        entry_name='Blass1984AOC',
        title='Existence of Bases Implies the Axiom of Choice',
        authors=[BibAuthor(main_name='Blass', other_names='Andreas')],
        language='english',
        journal='Contemporary Mathematics',
        publisher='American Mathematical Society (AMS)',
        url='http://www.math.lsa.umich.edu/ ablass/bases-AC.pdf',
        volume='31',
        year='1984'
    )


def test_arxiv_entry() -> None:
    string = dedent(r'''
        @article{Anderson1988NonEuclidean,
          author = {Anderson, Donald D.},
          doi = {10.1080/00927878808823628},
          journal = {Communications in Algebra},
          language = {english},
          month = {1},
          number = {6},
          pages = {1221-1229},
          primaryclass = {Algebra and Number Theory},
          publisher = {Informa UK Limited},
          title = {An Existence Theorem for Non-Euclidean PID's},
          url = {http://dx.doi.org/10.1080/00927878808823628},
          volume = {16},
          year = {1988}
        }
        '''[1:]
    )

    entries = parse_bibtex(string)
    assert len(entries) == 1
    assert entries[0] == BibEntry(
        entry_type='article',
        entry_name='Anderson1988NonEuclidean',
        title='An Existence Theorem for Non-Euclidean PID\'s',
        authors=[BibAuthor(main_name='Anderson', other_names='Donald D.')],
        language='english',
        journal='Communications in Algebra',
        doi='10.1080/00927878808823628',
        month='1',
        number='6',
        pages='1221-1229',
        primaryclass='Algebra and Number Theory',
        publisher='Informa UK Limited',
        url='http://dx.doi.org/10.1080/00927878808823628',
        volume='16',
        year='1988'
    )
