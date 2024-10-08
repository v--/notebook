from textwrap import dedent

import loguru
import pytest

from notebook.bibtex.parsing import parse_bibtex
from notebook.bibtex.string import VerbatimString

from .formatting import adjust_entry


def test_author_name_reformatting() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {Левенштейн, Владимир},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              date = {1965}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.authors[0].full_name == 'Владимир Левенштейн'


def test_author_name_verbatim() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {{Левенштейн, Владимир}},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              date = {1965}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.authors[0].full_name == VerbatimString('Левенштейн, Владимир')


def test_author_short() -> None:
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
    assert adjusted.authors[0].short_name == 'Levenshteyn'


def test_author_short_existing() -> None:
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
    assert adjusted.authors[0].short_name == 'Levenshtein'


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
    assert adjusted.languages == ['russian']


def test_missing_date(caplog: pytest.LogCaptureFixture) -> None:
    message = 'The date field is blank'
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965ДвоичныеКоды,
              author = {Владимир Левенштейн},
              language = {russian},
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
              author = {Henk Barendregt},
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
              author = {Henk Barendregt},
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
              author = {Henk Barendregt},
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
              author = {Samuel Eilenberg and Saunders Mac Lane},
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


def test_missing_eprint_type_and_id(caplog: pytest.LogCaptureFixture) -> None:
    message = "No eprint type or id specified for class 'math.HO'"
    entry, = parse_bibtex(
        dedent('''\
            @article{GreshamEtAl2019Trigonometry,
              author = {John Gresham and Bryant Wyatt and Jesse Crawford},
              date = {2019-01-01},
              eprintclass = {math.HO},
              language = {english},
              title = {Essential Trignometry Without Geometry}
            }
            '''
        )
    )

    with caplog.at_level('WARNING'):
        adjust_entry(entry, loguru.logger)
        assert message in caplog.text


def test_missing_eprint_type(caplog: pytest.LogCaptureFixture) -> None:
    message = "No eprint type specified for '1906.07050v1'"
    entry, = parse_bibtex(
        dedent('''\
            @article{GreshamEtAl2019Trigonometry,
              author = {John Gresham and Bryant Wyatt and Jesse Crawford},
              date = {2019-01-01},
              eprint = {1906.07050v1},
              language = {english},
              title = {Essential Trignometry Without Geometry}
            }
            '''
        )
    )

    with caplog.at_level('WARNING'):
        adjust_entry(entry, loguru.logger)
        assert message in caplog.text


def test_missing_eprint(caplog: pytest.LogCaptureFixture) -> None:
    message = "No eprint id specified for type 'arXiv'"
    entry, = parse_bibtex(
        dedent('''\
            @article{GreshamEtAl2019Trigonometry,
              author = {John Gresham and Bryant Wyatt and Jesse Crawford},
              date = {2019-01-01},
              eprintclass = {math.HO},
              eprinttype = {arXiv},
              language = {english},
              title = {Essential Trignometry Without Geometry}
            }
            '''
        )
    )

    with caplog.at_level('WARNING'):
        adjust_entry(entry, loguru.logger)
        assert message in caplog.text


def test_missing_arxiv_class(caplog: pytest.LogCaptureFixture) -> None:
    message = "No eprint class specified for arXiv entry '1906.07050v1'"
    entry, = parse_bibtex(
        dedent('''\
            @article{GreshamEtAl2019Trigonometry,
              author = {John Gresham and Bryant Wyatt and Jesse Crawford},
              date = {2019-01-01},
              eprint = {1906.07050v1},
              eprinttype = {arXiv},
              language = {english},
              title = {Essential Trignometry Without Geometry}
            }
            '''
        )
    )

    with caplog.at_level('WARNING'):
        adjust_entry(entry, loguru.logger)
        assert message in caplog.text


def test_arxiv_entry_url() -> None:
    entry, = parse_bibtex(
        dedent('''\
            @article{GreshamEtAl2019Trigonometry,
              author = {John Gresham and Bryant Wyatt and Jesse Crawford},
              date = {2019-01-01},
              eprint = {http://arxiv.org/abs/1906.07050v1},
              eprintclass = {math.HO},
              eprinttype = {arXiv},
              language = {english},
              title = {Essential Trignometry Without Geometry}
            }
            '''
        )
    )

    adjusted = adjust_entry(entry, loguru.logger)
    assert adjusted.eprint == '1906.07050v1'


def test_mathnet_url(caplog: pytest.LogCaptureFixture) -> None:
    message = 'Extracting a mathnet identifier from the URL'
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965,
              author = {Владимир Левенштейн},
              date = {1965},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              url = {http://mi.mathnet.ru/tm1095}
            }
            '''
        )
    )

    with caplog.at_level('INFO'):
        adjust_entry(entry, loguru.logger)
        assert message in caplog.text


def test_redundant_mathnet_url(caplog: pytest.LogCaptureFixture) -> None:
    message = 'Removing redundant mathnet URL'
    entry, = parse_bibtex(
        dedent('''\
            @article{Левенштейн1965,
              author = {Владимир Левенштейн},
              date = {1965},
              language = {russian},
              title = {Двоичные коды с исправлением выпадений, вставок и замещений символов},
              mathnet = {dan31411},
              url = {http://mi.mathnet.ru/dan31411}
            }
            '''
        )
    )

    with caplog.at_level('INFO'):
        adjust_entry(entry, loguru.logger)
        assert message in caplog.text
