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
    entry = mathnet_entry_to_bib(res, identifier, english=False)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='Левенштейн1965ДвоичныеКоды',
        title='Двоичные коды с исправлением выпадений, вставок и замещений символов',
        authors=[BibAuthor(full_name='В. И. Левенштейн')],
        languages=['russian'],
        date='1965',
        journal='Докл. АН СССР',
        volume='163',
        issue='4',
        pages='845-848',
        mathnet=identifier,
        mathscinet='0189928',
        zbmath='0149.15905'
    )


def test_parse_sm5974_rus(identifier: str = 'sm5974') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=False)
    entry = mathnet_entry_to_bib(res, identifier, english=False)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='Зыков1949НекоторыхСвойствахЛинейныхКомплексов',
        title='О некоторых свойствах линейных комплексов',
        authors=[BibAuthor(full_name='А. А. Зыков')],
        languages=['russian'],
        date='1949',
        journal='Матем. сб.',
        issue='2',
        volume='24(66)',
        pages='163-188',
        mathnet=identifier,
        mathscinet='35428',
        zbmath='0033.02602'
    )


def test_parse_tm1095_rus_no_journal(identifier: str = 'tm1095') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=False)
    entry = mathnet_entry_to_bib(res, identifier, english=False)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='АлександровУрысон1950КомпактныхТопологическихПространствах',
        title='О компактных топологических пространствах',
        authors=[BibAuthor(full_name='П. С. Александров'), BibAuthor(full_name='П. С. Урысон')],
        languages=['russian'],
        publisher='Изд-во АН СССР',
        date='1950',
        series='Тр. МИАН СССР',
        volume='31',
        pages='3-95',
        mathnet=identifier,
        mathscinet='43445',
        zbmath='0041.31504'
    )


def test_parse_sm274_rus_modern(identifier: str = 'sm274') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=False)
    entry = mathnet_entry_to_bib(res, identifier, english=False)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='МагарилИльяевТихомиров1997ПроизводныхКолмогоровскогоТипа',
        title='О неравенствах для производных колмогоровского типа',
        authors=[BibAuthor(full_name='Г. Г. Магарил-Ильяев'), BibAuthor(full_name='В. М. Тихомиров')],
        languages=['russian'],
        date='1997',
        issue='12',
        journal='Матем. сб.',
        volume='188',
        pages='73-106',
        mathnet=identifier,
        doi='10.4213/sm274',
        mathscinet='1607438',
        zbmath='0911.26009'
    )


def test_parse_sm274_eng_modern(identifier: str = 'sm274') -> None:
    with get_mathnet_fixture_path(identifier).open() as file:
        html = file.read()

    res = parse_mathnet_html(html, english=True)
    entry = mathnet_entry_to_bib(res, identifier, english=True)
    assert entry == BibEntry(
        entry_type='article',
        entry_name='MagarilIlYaevTikhomirov1997KolmogorovTypeInequalities',
        title='Kolmogorov-type inequalities for derivatives',
        authors=[BibAuthor(full_name="G. G. Magaril-Il'yaev"), BibAuthor(full_name='V. M. Tikhomirov')],
        languages=['english'],
        date='1997',
        issue='12',
        journal='Sb. Math.',
        volume='188',
        pages='1799-1832',
        mathnet=identifier,
        doi='10.1070/sm1997v188n12ABEH000274',
        mathscinet='1607438',
        zbmath='0911.26009',
        scopus='2-s2.0-0031284172'
    )
