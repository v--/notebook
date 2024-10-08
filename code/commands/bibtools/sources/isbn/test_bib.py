
from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry

from .bib import isbn_book_to_bib
from .fixtures import get_isbn_fixture_path
from .model import parse_isbn_json


def test_parse_9783961340057_empty_response(isbn: str = '978-3-96134-005-7') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 0


def test_parse_9780821810255(isbn: str = '978-0-8218-1025-5') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1
    entry = isbn_book_to_bib(res.items[0], isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Birkhoff1940LatticeTheory',
        title='Lattice Theory',
        authors=[
            BibAuthor(full_name='Garrett Birkhoff')
        ],
        isbn=isbn,
        languages=['english'],
        date='1940-12-31'
    )


def test_parse_9780821847817_subtitle(isbn: str = '978-0-8218-4781-7') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1
    entry = isbn_book_to_bib(res.items[0], isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Aluffi2009Algebra',
        title='Algebra',
        subtitle='Chapter 0',
        authors=[
            BibAuthor(full_name='Paolo Aluffi')
        ],
        isbn=isbn,
        languages=['english'],
        date='2009'
    )


# The response here doesn't even contain the ISBN itself
def test_parse_3885380064_limited_data(isbn: str = '3-88538-006-4') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1
    entry = isbn_book_to_bib(res.items[0], isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Engelking1989GeneralTopology',
        title='General Topology',
        authors=[
            BibAuthor(full_name='Ryszard Engelking')
        ],
        languages=['english'],
        date='1989',
        isbn=isbn
    )


def test_parse_9781071635971_subtitle_and_no_year(isbn: str = '978-1-0716-3597-1') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1
    entry = isbn_book_to_bib(res.items[0], isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='SoiferMathematicalColoringBook',
        title='The New Mathematical Coloring Book',
        subtitle='Mathematics of Coloring and the Colorful Life of Its Creators',
        authors=[
            BibAuthor(full_name='Alexander Soifer')
        ],
        languages=['english'],
        isbn=isbn
    )


def test_parse_5898060227_russian(isbn: str = '5-89806-022-7') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1
    entry = isbn_book_to_bib(res.items[0], isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Шафаревич1999ОсновныеПонятияАлгебры',
        title='Основные понятия алгебры',
        authors=[
            BibAuthor(full_name='Игорь Ростиславович Шафаревич')
        ],
        languages=['russian'],
        date='1999',
        isbn=isbn
    )


def test_parse_9785922102667_empty_subtitle(isbn: str = '978-5-9221-0266-7') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1
    entry = isbn_book_to_bib(res.items[0], isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Колмогоров2004ФункциональногоАнализа',
        title='Элементы теории функций и функционального анализа',
        authors=[
            BibAuthor(full_name='Андрей Николаевич Колмогоров')
        ],
        languages=['russian'],
        date='2004',
        isbn=isbn
    )


def test_parse_9785922107785_bad_unicode(isbn: str = '978-5-9221-0778-5') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1
    entry = isbn_book_to_bib(res.items[0], isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Tyrtyshnikov2007MatrichnyiAnalizILineinaiAAlgebra',
        title='Matrichnyĭ analiz i lineĭnai͡a algebra',
        authors=[
            BibAuthor(full_name='Evgeniĭ Evgenʹevich Tyrtyshnikov')
        ],
        languages=['russian'],
        date='2007',
        isbn=isbn
    )


def test_parse_9548706733_bulgarian(isbn: str = '954-8706-73-3') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1
    entry = isbn_book_to_bib(res.items[0], isbn)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Станилов1997ДиференциалнаГеометрия',
        title='Диференциална геометрия',
        subtitle='Учебник за студентите от СУ Св. Климент Охридски',
        authors=[
            BibAuthor(full_name='Грозяо Станилов')
        ],
        languages=['bulgarian'],
        date='1997',
        isbn=isbn
    )


def test_parse_5791300166_no_authors(isbn: str = '5-7913-0016-6') -> None:
    with get_isbn_fixture_path(isbn).open() as file:
        json_body = file.read()

    res = parse_isbn_json(json_body)
    assert len(res.items) == 1

    entry = isbn_book_to_bib(res.items[0], isbn)
    assert entry == BibEntry(
        entry_type='book',
        entry_name='2000CambridgeCompanionToJung',
        title='Cambridge companion to Jung',
        authors=[],
        languages=['russian'],
        date='2000',
        isbn=isbn
    )
