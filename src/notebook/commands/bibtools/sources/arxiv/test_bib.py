import pytest
from xsdata.exceptions import ParserError

from .....bibtex.author import BibAuthor
from .....bibtex.entry import BibEntry
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
        entry_type='misc',
        entry_name='DienerMcKubreJordens2016ClassifyingMaterialImplications',
        title='Classifying Material Implications over Minimal Logic',
        authors=[
            BibAuthor(full_name='Hannes Diener'),
            BibAuthor(full_name='Maarten McKubre-Jordens')
        ],
        languages=['english'],
        eprinttype='arXiv',
        eprintclass='math.LO',
        eprint=arxiv_id,
        date='2016-06-26'
    )


def test_parse_2011_00412v3(arxiv_id: str = '2011.00412v3') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='misc',
        entry_name='Leinster2023LebesgueIntegration',
        title='A categorical derivation of Lebesgue integration',
        authors=[
            BibAuthor(full_name='Tom Leinster')
        ],
        edition='3',
        languages=['english'],
        eprinttype='arXiv',
        eprintclass='math.FA',
        eprint=arxiv_id,
        date='2023-01-30'
    )


def test_parse_1010_0824v13_russian(arxiv_id: str = '1010.0824v13') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='misc',
        entry_name='Akbarov2024MathematicalAnalysis',
        title='Mathematical analysis without gaps',
        authors=[
            BibAuthor(full_name='Sergei Akbarov')
        ],
        languages=['english'],  # This is supposed to be "Russian", but the arXiv API does not give us this information
        eprinttype='arXiv',
        eprintclass='math.CA',
        eprint=arxiv_id,
        date='2024-06-14',
        edition='13'
    )


def test_parse_0903_0340v3_doi_and_link_without_type(arxiv_id: str = '0903.0340v3') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='misc',
        entry_name='BaezStay2009RosettaStone',
        doi='10.1007/978-3-642-12821-9_2',
        title='Physics, Topology, Logic and Computation: A Rosetta Stone',
        authors=[
            BibAuthor(full_name='John C. Baez'),
            BibAuthor(full_name='Mike Stay')
        ],
        languages=['english'],
        eprinttype='arXiv',
        eprintclass='quant-ph',
        eprint=arxiv_id,
        edition='3',
        date='2009-06-06'
    )


def test_parse_2401_09270v1_title_line_break(arxiv_id: str = '2401.09270v1') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='misc',
        entry_name='Ambridge2024ConstructiveUnivalentMathematics',
        title='Exact Real Search: Formalised Optimisation and Regression in Constructive Univalent Mathematics',
        authors=[
            BibAuthor(full_name='Todd Waugh Ambridge')
        ],
        languages=['english'],
        eprinttype='arXiv',
        eprintclass='cs.LO',
        eprint=arxiv_id,
        date='2024-01-17'
    )


def test_parse_2403_06707v1_dashes_and_line_break_in_title(arxiv_id: str = '2403.06707v1') -> None:
    with get_arxiv_fixture_path(arxiv_id).open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    assert len(feed.entries) == 1
    entry = arxiv_entry_to_bib(feed.entries[0], arxiv_id)

    assert entry == BibEntry(
        entry_type='misc',
        entry_name='BinderEtAl2024DerivingDependentlyTypedOOP',
        title='Deriving Dependently-Typed OOP from First Principles -- Extended Version with Additional Appendices',
        authors=[
            BibAuthor(full_name='David Binder'),
            BibAuthor(full_name='Ingo Skupin'),
            BibAuthor(full_name='Tim Süberkrüb'),
            BibAuthor(full_name='Klaus Ostermann')
        ],
        doi='10.1145/3649846',
        languages=['english'],
        eprinttype='arXiv',
        eprintclass='cs.PL',
        eprint=arxiv_id,
        date='2024-03-11'
    )
