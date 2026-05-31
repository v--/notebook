import json

import stdnum.isbn

from notebook.bibtex import BibAuthor, BibEntry

from .bib import isbn_book_to_bib
from .fixtures import get_isbn_fixture_path
from .model import parse_isbn_json


def test_parse_9780821810255(isbn: str = '978-0-8218-1025-5') -> None:
    with get_isbn_fixture_path(stdnum.isbn.compact(isbn)).open() as file:
        book_json = json.load(file)

    book = parse_isbn_json(book_json)
    entry = isbn_book_to_bib(book, isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Birkhoff1979AmerMathematicalSoc',
        title='Lattice Theory (Colloquium Publications (Amer Mathematical Soc))',
        authors=[
            BibAuthor(full_name='Garrett Birkhoff'),
        ],
        languages=['english'],
        publishers=['American Mathematical Society'],
        isbn=isbn,
        date='December 1979',
    )


def test_parse_9780821847817(isbn: str = '978-0-8218-4781-7') -> None:
    with get_isbn_fixture_path(stdnum.isbn.compact(isbn)).open() as file:
        book_json = json.load(file)

    book = parse_isbn_json(book_json)
    entry = isbn_book_to_bib(book, isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Aluffi2009Algebra',
        title='Algebra',
        authors=[
            BibAuthor(full_name='Paolo Aluffi'),
        ],
        isbn=isbn,
        languages=['english'],
        publishers=['American Mathematical Society', 'Brand: American Mathematical Society'],
        date='2009',
    )


def test_parse_3885380064_polish(isbn: str = '3-88538-006-4') -> None:
    with get_isbn_fixture_path(stdnum.isbn.compact(isbn)).open() as file:
        book_json = json.load(file)

    book = parse_isbn_json(book_json)
    entry = isbn_book_to_bib(book, isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Engelking1989Topology',
        title='General topology',
        authors=[
            BibAuthor(full_name='Ryszard Engelking'),
        ],
        languages=['english', 'polish'],
        publishers=['Heldermann'],
        date='1989',
        isbn=isbn,
    )


def test_parse_9785922102667_russian(isbn: str = '978-5-9221-0266-7') -> None:
    with get_isbn_fixture_path(stdnum.isbn.compact(isbn)).open() as file:
        book_json = json.load(file)

    book = parse_isbn_json(book_json)
    entry = isbn_book_to_bib(book, isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Колмогоров2006ÉлементыТеорииФункций',
        title='Éлементы теории функций и функционалЬного анализа',
        authors=[
            BibAuthor(full_name='Андреи Николаевич Колмогоров'),
        ],
        languages=['russian'],
        publishers=['Физматлит'],
        date='2006',
        isbn=isbn,
    )


def test_parse_9785922107785_bad_unicode(isbn: str = '978-5-9221-0778-5') -> None:
    with get_isbn_fixture_path(stdnum.isbn.compact(isbn)).open() as file:
        book_json = json.load(file)

    book = parse_isbn_json(book_json)
    entry = isbn_book_to_bib(book, isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Тыртышников2007МатричныĭАнализ',
        title='Матричныĭ анализ и линеĭнаи͡а алгебра',
        authors=[
            BibAuthor(full_name='Е. Е. Тыртышников'),
        ],
        languages=['russian'],
        date='2007',
        publishers=['Физматлит'],
        isbn=isbn,
    )


def test_parse_5791300166_toc_and_no_authors(isbn: str = '0-471-43334-9') -> None:
    with get_isbn_fixture_path(stdnum.isbn.compact(isbn)).open() as file:
        book_json = json.load(file)

    book = parse_isbn_json(book_json)
    entry = isbn_book_to_bib(book, isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='2004AbstractAlgebra',
        title='Abstract algebra',
        authors=[],
        languages=['english'],
        date='2004',
        publishers=['Wiley'],
        isbn=isbn,
    )
