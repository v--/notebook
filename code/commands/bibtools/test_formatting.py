from textwrap import dedent

import loguru
import pytest

from notebook.bibtex.parsing import parse_bibtex

from .formatting import adjust_entry


def test_author_name_reformatting() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {Владимир Левенштейн},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              date = {1965}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.authors[0].get_full_string() == 'Левенштейн, Владимир'


def test_author_name_verbatim() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {{Владимир Левенштейн}},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              date = {1965}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.authors[0].get_full_string() == 'Владимир Левенштейн'


def test_author_display_name() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {Владимир Левенштейн},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              date = {1965}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.authors[0].display_name == 'Levenshteyn'


def test_author_display_name_existing() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {Владимир Левенштейн},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              shortauthor = {Levenshtein},
              date = {1965}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.authors[0].display_name == 'Levenshtein'


def test_language_reformatting() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {Владимир Левенштейн},
              language = {ru},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              date = {1965}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.language == 'russian'


def test_missing_date(caplog: pytest.LogCaptureFixture) -> None:
    message = 'The date field is blank'
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {Владимир Левенштейн},
              language = {ru},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов}
            }
            '''
        )
    )

    with caplog.at_level('WARNING'):
        adjust_entry(entry, loguru.logger)
        assert message in caplog.text


def test_piecewise_date(caplog: pytest.LogCaptureFixture) -> None:
    message = 'The date field is blank'
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {Владимир Левенштейн},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              year = {1965},
              month = {2},
              day = {1}
            }
            '''
        )
    )

    with caplog.at_level('WARNING'):
        adjusted = adjust_entry(entry, loguru.logger)
        assert message not in caplog.text

    assert adjusted.date == '1965-02-01'
    assert adjusted.year is None
    assert adjusted.month is None
    assert adjusted.day is None


def test_title_splitting() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @book{Barendregt1984LambdaCalculus,
              author = {Barendregt, Henk},
              isbn = {0-444-86748-1},
              language = {english},
              publisher = {North-Holland},
              title = {The Lambda Calculus - Its Syntax and Semantics},
              date = {1984}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.title == 'The Lambda Calculus'
    assert adjusted.subtitle == 'Its Syntax and Semantics'


def test_title_splitting_with_subtitle() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @book{Barendregt1984LambdaCalculus,
              author = {Barendregt, Henk},
              isbn = {0-444-86748-1},
              language = {english},
              publisher = {North-Holland},
              title = {The Lambda Calculus - Its Syntax and Semantics},
              subtitle = {Test Subtitle},
              date = {1984}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.title == 'The Lambda Calculus - Its Syntax and Semantics'
    assert adjusted.subtitle == 'Test Subtitle'


def test_isbn_formatting() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @book{Barendregt1984LambdaCalculus,
              author = {Barendregt, Henk},
              isbn = {0444867481},
              language = {english},
              publisher = {North-Holland},
              title = {The Lambda Calculus},
              subtitle = {Its Syntax and Semantics},
              date = {1984}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.isbn == '0-444-86748-1'


def test_issn_formatting() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{Eilenberg1945Equivalences,
              author = {Eilenberg, Samuel and MacLane, Saunders},
              date = {1945-09},
              doi = {10.2307/1990284},
              issn = {00029947},
              journal = {Transactions of the American Mathematical Society},
              language = {english},
              pages = {231},
              publisher = {JSTOR},
              title = {General Theory of Natural Equivalences},
              url = {http://dx.doi.org/10.2307/1990284},
              volume = {58}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.issn == '0002-9947'
