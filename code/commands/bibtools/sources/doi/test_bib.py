from notebook.bibtex.author import BibAuthor
from notebook.bibtex.entry import BibEntry

from .bib import doi_data_to_bib
from .fixtures import get_doi_fixture_path
from .model import parse_doi_json


def test_parse_1023072266967(doi: str = '10.2307/2266967') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi, print_edition=True)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Henkin1950Theory',
        title='Completeness in the theory of types',
        publisher='Cambridge University Press (CUP)',
        journal='Journal of Symbolic Logic',
        authors=[
            BibAuthor(main_name='Henkin', other_names='Leon')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        date='1950-06',
        issn='0022-4812,1943-5886',
        volume='15',
        pages='81-91'
    )



def test_parse_1023072266967_electronic_edition(doi: str = '10.2307/2266967') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi, print_edition=False)

    assert entry.date == '2014-03-12'


def test_parse_101215_ijm_1256049011_missing_fields(doi: str = '10.1215/ijm/1256049011') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Appel1977PlanarMap',
        title='Every planar map is four colorable',
        subtitle='Part I: Discharging',
        publisher='Duke University Press',
        journal='Illinois Journal of Mathematics',
        authors=[
            BibAuthor(main_name='Appel', other_names='K.'),
            BibAuthor(main_name='Haken', other_names='W.')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        date='1977-09-01',
        issn='0019-2082',
        volume='21'
    )


def test_parse_101215_ijm_1256049012_missing_fields(doi: str = '10.1215/ijm/1256049012') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Appel1977PlanarMap',
        title='Every planar map is four colorable',
        subtitle='Part II: Reducibility',
        publisher='Duke University Press',
        journal='Illinois Journal of Mathematics',
        authors=[
            BibAuthor(main_name='Appel', other_names='K.'),
            BibAuthor(main_name='Haken', other_names='W.'),
            BibAuthor(main_name='Koch', other_names='J.')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        date='1977-09-01',
        issn='0019-2082',
        volume='21'
    )


def test_parse_101134_s0081543815090023_references(doi: str = '10.1134/s0081543815090023') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Aseev2015InfiniteHorizonOptimalControlProblems',
        title='Maximum principle for infinite-horizon optimal control problems under weak regularity assumptions',
        publisher='Pleiades Publishing Ltd',
        journal='Proceedings of the Steklov Institute of Mathematics',
        authors=[
            BibAuthor(main_name='Aseev', other_names='S. M.'),
            BibAuthor(main_name='Veliov', other_names='V. M.')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        date='2015-12-11',
        issn='0081-5438,1531-8605',
        volume='291',
        pages='22-39'
    )


def test_parse_101016_jindag201901001_assertions(doi: str = '10.1016/j.indag.2019.01.001') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi, print_edition=True)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Bezhanishvili2019IntuitionisticLogic',
        title='A semantic hierarchy for intuitionistic logic',
        publisher='Elsevier BV',
        journal='Indagationes Mathematicae',
        authors=[
            BibAuthor(main_name='Bezhanishvili', other_names='Guram'),
            BibAuthor(main_name='Holliday', other_names='Wesley H.')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        date='2019-05',
        issn='0019-3577',
        volume='30',
        pages='403-469'
    )


def test_parse_101016_jjmaa2019123445_funder(doi: str = '10.1016/j.jmaa.2019.123445') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Bivas2020TangentialTransversality',
        title='On tangential transversality',
        publisher='Elsevier BV',
        authors=[
            BibAuthor(main_name='Bivas', other_names='Mira'),
            BibAuthor(main_name='Krastanov', other_names='Mikhail'),
            BibAuthor(main_name='Ribarska', other_names='Nadezhda')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        journal='Journal of Mathematical Analysis and Applications',
        volume='481',
        date='2020-01',
        issn='0022-247X',
        pages='123445'
    )


def test_parse_101145_13274521327492_assertion_order_and_group(doi: str = '10.1145/1327452.1327492') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Dean2008SimplifiedDataProcessing',
        title='MapReduce',
        subtitle='simplified data processing on large clusters',
        publisher='Association for Computing Machinery (ACM)',
        authors=[
            BibAuthor(main_name='Dean', other_names='Jeffrey'),
            BibAuthor(main_name='Ghemawat', other_names='Sanjay')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        journal='Communications of the ACM',
        volume='51',
        pages='107-113',
        date='2008-01',
        issn='0001-0782,1557-7317'
    )


def test_parse_102307_4145127_reference_edition(doi: str = '10.2307/4145127') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi, print_edition=True)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Edelman2004PascalMatrices',
        title='Pascal Matrices',
        publisher='Informa UK Limited',
        authors=[
            BibAuthor(main_name='Edelman', other_names='Alan'),
            BibAuthor(main_name='Strang', other_names='Gilbert')
        ],
        doi=doi,
        url='http://dx.doi.org/10.1080/00029890.2004.11920065',
        language='english',
        journal='The American Mathematical Monthly',
        volume='111',
        pages='189-197',
        date='2004-03',
        issn='0002-9890,1930-0972'
    )


def test_parse_101090_bull_1616_reference_issn(doi: str = '10.1090/bull/1616') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Grayson2018UnivalentFoundations',
        title='An introduction to univalent foundations for mathematicians',
        publisher='American Mathematical Society (AMS)',
        authors=[
            BibAuthor(main_name='Grayson', other_names='Daniel')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        journal='Bulletin of the American Mathematical Society',
        volume='55',
        pages='427-450',
        date='2018-03-05',
        issn='0273-0979,1088-9485'
    )


def test_parse_101007_s1065401601493_extended_funder(doi: str = '10.1007/s10654-016-0149-3') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Greenland2016StatisticalTests',
        title='Statistical tests, P values, confidence intervals, and power',
        subtitle='a guide to misinterpretations',
        publisher='Springer Science and Business Media LLC',
        authors=[
            BibAuthor(main_name='Greenland', other_names='Sander'),
            BibAuthor(main_name='Senn', other_names='Stephen J.'),
            BibAuthor(main_name='Rothman', other_names='Kenneth J.'),
            BibAuthor(main_name='Carlin', other_names='John B.'),
            BibAuthor(main_name='Poole', other_names='Charles'),
            BibAuthor(main_name='Goodman', other_names='Steven N.'),
            BibAuthor(main_name='Altman', other_names='Douglas G.')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        journal='European Journal of Epidemiology',
        volume='31',
        pages='337-350',
        date='2016-05-21',
        issn='0393-2990,1573-7284'
    )


def test_parse_101016_jentcs200409017_special_numbering(doi: str = '10.1016/j.entcs.2004.09.017') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Escardo2004SyntheticTopology',
        title='Synthetic Topology',
        publisher='Elsevier BV',
        authors=[
            BibAuthor(main_name='Escardó', other_names='Martín')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        journal='Electronic Notes in Theoretical Computer Science',
        volume='87',
        pages='21-156',
        date='2004-11',
        issn='1571-0661'
    )


def test_parse_101111_tops12019_updated_by(doi: str = '10.1111/tops.12019') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Inglis2013EvaluatingElementaryProofs',
        title="On Mathematicians' Different Standards When Evaluating Elementary Proofs",
        publisher='Wiley',
        authors=[
            BibAuthor(main_name='Inglis', other_names='Matthew'),
            BibAuthor(main_name='Mejia‐Ramos', other_names='Juan Pablo'),
            BibAuthor(main_name='Weber', other_names='Keith'),
            BibAuthor(main_name='Alcock', other_names='Lara')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        journal='Topics in Cognitive Science',
        volume='5',
        pages='270-282',
        date='2013-04-11',
        issn='1756-8757,1756-8765'
    )


def test_parse_101007_97836421282192_book(doi: str = '10.1007/978-3-642-66451-9') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Bergh1976InterpolationSpaces',
        title='Interpolation Spaces',
        subtitle='An Introduction',
        publisher='Springer Berlin Heidelberg',
        authors=[
            BibAuthor(main_name='Bergh', other_names='Jöran'),
            BibAuthor(main_name='Löfström', other_names='Jörgen')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        series='Grundlehren der mathematischen Wissenschaften',
        date='1976',
        issn='0072-7830',
        isbn='978-3-642-66451-9'
    )


def test_parse_101007_9783319114781_book(doi: str = '10.1007/978-3-319-11478-1') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi, print_edition=True)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Bergman2015GeneralAlgebra',
        title='An Invitation to General Algebra and Universal Constructions',
        publisher='Springer International Publishing',
        authors=[
            BibAuthor(main_name='Bergman', other_names='George M.')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        series='Universitext',
        date='2015',
        issn='0172-5939,2191-6675',
        isbn='978-3-319-11477-4'
    )


def test_parse_101007_97836421282192_book_chapter(doi: str = '10.1007/978-3-642-12821-9_2') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='inbook',
        entry_name='Baez2010RosettaStone',
        title='Physics, Topology, Logic and Computation',
        subtitle='A Rosetta Stone',
        publisher='Springer Berlin Heidelberg',
        authors=[
            BibAuthor(main_name='Baez', other_names='J.'),
            BibAuthor(main_name='Stay', other_names='M.')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        series='Lecture Notes in Physics',
        date='2010-07-05',
        issn='0075-8450,1616-6361',
        isbn='978-3-642-12821-9',
        pages='95-172'
    )


def test_parse_101007_9783642617010_container_empty_array(doi: str = '10.1007/978-3-642-61701-0') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Bourbaki1995GeneralTopology',
        title='General Topology',
        subtitle='Chapters 1–4',
        publisher='Springer Berlin Heidelberg',
        authors=[
            BibAuthor(main_name='Bourbaki', other_names='Nicolas')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        language='english',
        date='1995',
        isbn='978-3-642-61701-0'
    )


def test_parse_101017_9781108583664_edition_and_no_links(doi: str = '10.1017/9781108583664') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='Boyd2019AppliedLinearAlgebra',
        title='Introduction to Applied Linear Algebra',
        subtitle='Vectors, Matrices, and Least Squares',
        publisher='Cambridge University Press & Assessment',
        authors=[
            BibAuthor(main_name='Boyd', other_names='Stephen'),
            BibAuthor(main_name='Vandenberghe', other_names='Lieven')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        edition='1',
        language='english',
        date='2019-09-13',
        isbn='978-1-108-58366-4'
    )


def test_parse_101109_ieeestd20198766229_standard(doi: str = '10.1109/IEEESTD.2019.8766229') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='misc',
        entry_name='IeeeIeeeStandard',
        title='IEEE Standard for Floating-Point Arithmetic',
        publisher='IEEE',
        authors=[
            BibAuthor(main_name='IEEE')
        ],
        doi=doi,
        url=f'http://dx.doi.org/{doi}',
        isbn='978-1-5044-5924-2',
        language='english',
    )
