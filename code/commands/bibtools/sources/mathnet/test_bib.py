import pytest

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry

from ...exceptions import BibToolsNotFoundError, BibToolsParsingError
from .bib import mathnet_entry_to_bib
from .fixtures import get_mathnet_fixture_path
from .model import parse_mathnet_html


def test_parse_invalid(identifier: str = 'invalid') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    with pytest.raises(BibToolsParsingError):
        parse_mathnet_html(html, english=False)


def test_parse_dan31411_eng(identifier: str = 'dan31411') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    with pytest.raises(BibToolsNotFoundError):
        parse_mathnet_html(html, english=True)


def test_parse_dan31411_rus(identifier: str = 'dan31411') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=False)
    entry = mathnet_entry_to_bib(res, english=False)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='Левенштейн1965ДвоичныеКоды',
        title='Двоичные коды с исправлением выпадений, вставок и замещений символов',
        authors=[BibAuthor(main_name='Левенштейн', other_names='В. И.')],
        language='russian',
        date='1965',
        journal='Докл. АН СССР',
        volume='163',
        issue='4',
        pages='845--848',
        url=f'http://mi.mathnet.ru/{identifier}',
        mathscinet='http://mathscinet.ams.org/mathscinet-getitem?mr=0189928',
        zmath='https://zbmath.org/?q=an:0149.15905'
    )


def test_parse_sm5974_rus(identifier: str = 'sm5974') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=False)
    entry = mathnet_entry_to_bib(res, english=False)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='Зыков1949НекоторыхСвойствахЛинейныхКомплексов',
        title='О некоторых свойствах линейных комплексов',
        authors=[BibAuthor(main_name='Зыков', other_names='А. А.')],
        language='russian',
        date='1949',
        journal='Матем. сб.',
        issue='2',
        volume='24(66)',
        pages='163--188',
        url=f'http://mi.mathnet.ru/{identifier}',
        mathscinet='http://mathscinet.ams.org/mathscinet-getitem?mr=35428',
        zmath='https://zbmath.org/?q=an:0033.02602'
    )


def test_parse_tm1095_rus_no_journal(identifier: str = 'tm1095') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=False)
    entry = mathnet_entry_to_bib(res, english=False)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='АлександровУрысон1950КомпактныхТопологическихПространствах',
        title='О компактных топологических пространствах',
        authors=[BibAuthor(main_name='Александров', other_names='П. С.'), BibAuthor(main_name='Урысон', other_names='П. С.')],
        language='russian',
        publisher='Изд-во АН СССР',
        date='1950',
        series='Тр. МИАН СССР',
        volume='31',
        pages='3--95',
        url=f'http://mi.mathnet.ru/{identifier}',
        mathscinet='http://mathscinet.ams.org/mathscinet-getitem?mr=43445',
        zmath='https://zbmath.org/?q=an:0041.31504'
    )


def test_parse_sm274_rus_modern(identifier: str = 'sm274') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=False)
    entry = mathnet_entry_to_bib(res, english=False)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='МагарилИльяевТихомиров1997ПроизводныхКолмогоровскогоТипа',
        title='О неравенствах для производных колмогоровского типа',
        authors=[BibAuthor(main_name='Магарил-Ильяев', other_names='Г. Г.'), BibAuthor(main_name='Тихомиров', other_names='В. М.')],
        language='russian',
        date='1997',
        issue='12',
        journal='Матем. сб.',
        volume='188',
        pages='73--106',
        url=f'http://mi.mathnet.ru/{identifier}',
        doi='https://doi.org/10.4213/sm274',
        mathscinet='http://mathscinet.ams.org/mathscinet-getitem?mr=1607438',
        zmath='https://zbmath.org/?q=an:0911.26009'
    )


def test_parse_sm274_eng_modern(identifier: str = 'sm274') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=True)
    entry = mathnet_entry_to_bib(res, english=True)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='MagarilIlYaevTikhomirov1997KolmogorovTypeInequalities',
        title='Kolmogorov-type inequalities for derivatives',
        authors=[BibAuthor(main_name="Magaril-Il'yaev", other_names='G. G.'), BibAuthor(main_name='Tikhomirov', other_names='V. M.')],
        language='english',
        date='1997',
        issue='12',
        journal='Sb. Math.',
        volume='188',
        pages='1799--1832',
        url=f'http://mi.mathnet.ru/{identifier}',
        doi='https://doi.org/10.1070/sm1997v188n12ABEH000274',
        mathscinet='http://mathscinet.ams.org/mathscinet-getitem?mr=1607438',
        zmath='https://zbmath.org/?q=an:0911.26009',
        scopus='https://www.scopus.com/record/display.url?origin=inward&eid=2-s2.0-0031284172'
    )
