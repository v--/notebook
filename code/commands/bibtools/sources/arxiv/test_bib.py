import pytest
from xsdata.exceptions import ParserError

from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry

from .bib import arxiv_entry_to_bib
from .fixtures import get_arxiv_fixture_path
from .model import parse_arxiv_xml


def test_parse_incompatible() -> None:
    with get_arxiv_fixture_path('incompatible').open() as file:
        xml_body = file.read()

    # It is only a parser error in case of unrecognized fields
    with pytest.raises(ParserError):
        parse_arxiv_xml(xml_body)


# arXiv gives us invalid entries for future versions
# At the time of writing this test, v4 did not exist (see v3 below), but we have an invalid entry cached here
def test_parse_2011_00412v4(arxiv_id: str = '2011.00412v4') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    # It is only a type error in case of insufficiently many fields
    with pytest.raises(TypeError):
        parse_arxiv_xml(xml_body)


def test_parse_no_entries() -> None:
    with get_arxiv_fixture_path('no_entries').open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 0


def test_parse_1606_08092v1(arxiv_id: str = '1606.08092v1') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='DienerMcKubreJordens2016ClassifyingMaterialImplications',
        title='Classifying Material Implications over Minimal Logic',
        authors=[
            BibAuthor(main_name='Diener', other_names='Hannes'),
            BibAuthor(main_name='McKubre-Jordens', other_names='Maarten')
        ],
        language='english',
        archiveprefix='arXiv',
        primaryclass='math.LO',
        eprint=arxiv_id,
        date='2016-06-26',
        url=f'http://arxiv.org/abs/{arxiv_id}'
    )


def test_parse_2011_00412v3(arxiv_id: str = '2011.00412v3') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Leinster2023LebesgueIntegration',
        title='A categorical derivation of Lebesgue integration',
        authors=[
            BibAuthor(main_name='Leinster', other_names='Tom')
        ],
        edition='3',
        language='english',
        archiveprefix='arXiv',
        primaryclass='math.FA',
        eprint=arxiv_id,
        date='2023-01-30',
        url=f'http://arxiv.org/abs/{arxiv_id}'
    )


def test_parse_1010_0824v13_russian(arxiv_id: str = '1010.0824v13') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Akbarov2024MathematicalAnalysis',
        title='Mathematical analysis without gaps',
        authors=[
            BibAuthor(main_name='Akbarov', other_names='Sergei')
        ],
        language='english',  # This is supposed to be "Russian", but the arXiv API does not give us this information
        archiveprefix='arXiv',
        primaryclass='math.CA',
        eprint=arxiv_id,
        date='2024-06-14',
        edition='13',
        url=f'http://arxiv.org/abs/{arxiv_id}'
    )


def test_parse_0903_0340v3_doi_and_link_without_type(arxiv_id: str = '0903.0340v3') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='BaezStay2009RosettaStone',
        doi='10.1007/978-3-642-12821-9_2',
        title='Physics, Topology, Logic and Computation',
        subtitle='A Rosetta Stone',
        authors=[
            BibAuthor(main_name='Baez', other_names='John C.'),
            BibAuthor(main_name='Stay', other_names='Mike')
        ],
        language='english',
        archiveprefix='arXiv',
        primaryclass='quant-ph',
        eprint=arxiv_id,
        edition='3',
        date='2009-06-06',
        url=f'http://arxiv.org/abs/{arxiv_id}'
    )


def test_parse_2401_09270v1_title_line_break(arxiv_id: str = '2401.09270v1') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Ambridge2024ExactRealSearch',
        title='Exact Real Search',
        subtitle='Formalised Optimisation and Regression in Constructive Univalent Mathematics',
        authors=[
            BibAuthor(main_name='Ambridge', other_names='Todd Waugh')
        ],
        language='english',
        archiveprefix='arXiv',
        primaryclass='cs.LO',
        eprint=arxiv_id,
        date='2024-01-17',
        url=f'http://arxiv.org/abs/{arxiv_id}'
    )


def test_parse_2403_06707v1_dashes_in_title(arxiv_id: str = '2403.06707v1') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='BinderEtAl2024DerivingDependentlyTypedOOP',
        title='Deriving Dependently-Typed OOP from First Principles',
        subtitle='Extended Version with Additional Appendices',
        authors=[
            BibAuthor(main_name='Binder', other_names='David'),
            BibAuthor(main_name='Skupin', other_names='Ingo'),
            BibAuthor(main_name='Süberkrüb', other_names='Tim'),
            BibAuthor(main_name='Ostermann', other_names='Klaus')
        ],
        doi='10.1145/3649846',
        language='english',
        archiveprefix='arXiv',
        primaryclass='cs.PL',
        eprint=arxiv_id,
        date='2024-03-11',
        url=f'http://arxiv.org/abs/{arxiv_id}'
    )
