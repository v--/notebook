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
            BibAuthor(full_name='Leon Henkin')
        ],
        doi=doi,
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
        entry_name='AppelHaken1977PlanarMap',
        title='Every planar map is four colorable',
        subtitle='Part I: Discharging',
        publisher='Duke University Press',
        journal='Illinois Journal of Mathematics',
        authors=[
            BibAuthor(full_name='K. Appel'),
            BibAuthor(full_name='W. Haken')
        ],
        doi=doi,
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
        entry_name='AppelEtAl1977PlanarMap',
        title='Every planar map is four colorable',
        subtitle='Part II: Reducibility',
        publisher='Duke University Press',
        journal='Illinois Journal of Mathematics',
        authors=[
            BibAuthor(full_name='K. Appel'),
            BibAuthor(full_name='W. Haken'),
            BibAuthor(full_name='J. Koch')
        ],
        doi=doi,
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
        entry_name='AseevVeliov2015InfiniteHorizonOptimalControlProblems',
        title='Maximum principle for infinite-horizon optimal control problems under weak regularity assumptions',
        publisher='Pleiades Publishing Ltd',
        journal='Proceedings of the Steklov Institute of Mathematics',
        authors=[
            BibAuthor(full_name='S. M. Aseev'),
            BibAuthor(full_name='V. M. Veliov')
        ],
        doi=doi,
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
        entry_name='BezhanishviliHolliday2019IntuitionisticLogic',
        title='A semantic hierarchy for intuitionistic logic',
        publisher='Elsevier BV',
        journal='Indagationes Mathematicae',
        authors=[
            BibAuthor(full_name='Guram Bezhanishvili'),
            BibAuthor(full_name='Wesley H. Holliday')
        ],
        doi=doi,
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
        entry_name='BivasEtAl2020TangentialTransversality',
        title='On tangential transversality',
        publisher='Elsevier BV',
        authors=[
            BibAuthor(full_name='Mira Bivas'),
            BibAuthor(full_name='Mikhail Krastanov'),
            BibAuthor(full_name='Nadezhda Ribarska')
        ],
        doi=doi,
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
        entry_name='DeanGhemawat2008SimplifiedDataProcessing',
        title='MapReduce',
        subtitle='simplified data processing on large clusters',
        publisher='Association for Computing Machinery (ACM)',
        authors=[
            BibAuthor(full_name='Jeffrey Dean'),
            BibAuthor(full_name='Sanjay Ghemawat')
        ],
        doi=doi,
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
        entry_name='EdelmanStrang2004PascalMatrices',
        title='Pascal Matrices',
        publisher='Informa UK Limited',
        authors=[
            BibAuthor(full_name='Alan Edelman'),
            BibAuthor(full_name='Gilbert Strang')
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
            BibAuthor(full_name='Daniel Grayson')
        ],
        doi=doi,
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
        entry_name='GreenlandEtAl2016StatisticalTests',
        title='Statistical tests, P values, confidence intervals, and power',
        subtitle='a guide to misinterpretations',
        publisher='Springer Science and Business Media LLC',
        authors=[
            BibAuthor(full_name='Sander Greenland'),
            BibAuthor(full_name='Stephen J. Senn'),
            BibAuthor(full_name='Kenneth J. Rothman'),
            BibAuthor(full_name='John B. Carlin'),
            BibAuthor(full_name='Charles Poole'),
            BibAuthor(full_name='Steven N. Goodman'),
            BibAuthor(full_name='Douglas G. Altman')
        ],
        doi=doi,
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
            BibAuthor(full_name='Martín Escardó')
        ],
        doi=doi,
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
        entry_name='InglisEtAl2013EvaluatingElementaryProofs',
        title="On Mathematicians' Different Standards When Evaluating Elementary Proofs",
        publisher='Wiley',
        authors=[
            BibAuthor(full_name='Matthew Inglis'),
            BibAuthor(full_name='Juan Pablo Mejia‐Ramos'),
            BibAuthor(full_name='Keith Weber'),
            BibAuthor(full_name='Lara Alcock')
        ],
        doi=doi,
        language='english',
        journal='Topics in Cognitive Science',
        volume='5',
        pages='270-282',
        date='2013-04-11',
        issn='1756-8757,1756-8765'
    )


def test_parse_101145_3649846_orcid(doi: str = '10.1145/3649846') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='BinderEtAl2024DerivingDependentlyTypedOOP',
        title='Deriving Dependently-Typed OOP from First Principles',
        authors=[
            BibAuthor(full_name='David Binder'),
            BibAuthor(full_name='Ingo Skupin'),
            BibAuthor(full_name='Tim Süberkrüb'),
            BibAuthor(full_name='Klaus Ostermann'),
        ],
        doi=doi,
        language='english',
        publisher='Association for Computing Machinery (ACM)',
        journal='Proceedings of the ACM on Programming Languages',
        volume='8',
        pages='983-1009',
        date='2024-04-29',
        issn='2475-1421'
    )


def test_parse_1048550_arxiv180905923(doi: str = '10.48550/arXiv.1809.05923') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='BradleyAppliedCategoryTheory',
        title='What is Applied Category Theory?',
        authors=[
            BibAuthor(full_name='Tai-Danae Bradley')
        ],
        doi=doi,
        url='https://arxiv.org/abs/1809.05923',
        language='english',
        publisher='arXiv'
    )


def test_parse_101109_mc19871663532_no_given_name(doi: str = '10.1109/MC.1987.1663532') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Brooks1987SilverBulletEssence',
        title='No Silver Bullet Essence and Accidents of Software Engineering',
        authors=[
            BibAuthor(full_name='Brooks')
        ],
        doi=doi,
        date='1987-04',
        publisher='Institute of Electrical and Electronics Engineers (IEEE)',
        language='english',
        journal='Computer',
        volume='20',
        pages='10-19',
        issn='0018-9162'
    )


def test_parse_104169_collegemathj475322_assertion_url(doi: str = '10.4169/college.math.j.47.5.322') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Kowalski2017SingleDegree',
        title='The Sine of a Single Degree',
        authors=[
            BibAuthor(full_name='Travis Kowalski')
        ],
        doi=doi,
        date='2017-11-27',
        publisher='Informa UK Limited',
        language='english',
        journal='The College Mathematics Journal',
        volume='47',
        pages='322-332',
        issn='0746-8342,1931-1346'
    )


def test_parse_103934_dcdsb2018020_no_family_name(doi: str = '10.3934/dcdsb.2018020') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='article',
        entry_name='Krukowski2018UniformSpaces',
        title="Arzelà-Ascoli's theorem in uniform spaces",
        authors=[
            BibAuthor(full_name='Mateusz Krukowski')
        ],
        doi=doi,
        date='2018',
        publisher='American Institute of Mathematical Sciences (AIMS)',
        language='english',
        journal='Discrete &amp; Continuous Dynamical Systems - B',
        volume='23',
        pages='283-294',
        issn='1553-524X'
    )


def test_parse_101007_9783662074138_editor(doi: str = '10.1007/978-3-662-07413-8') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='ArhangelSkii1995GeneralTopologyIII',
        title='General Topology III',
        publisher='Springer Berlin Heidelberg',
        authors=[
            BibAuthor(full_name='A. V. Arhangel’skii')
        ],
        editors=[
            BibAuthor(full_name='A. V. Arhangel’skii')
        ],
        doi=doi,
        language='english',
        date='1995',
        series='Encyclopaedia of Mathematical Sciences',
        isbn='978-3-662-07413-8',
        issn='0938-0396'
    )


def test_parse_101007_97836421282192_book(doi: str = '10.1007/978-3-642-66451-9') -> None:
    with get_doi_fixture_path(doi).open() as file:
        json_body = file.read()

    data = parse_doi_json(json_body)
    entry = doi_data_to_bib(data, doi)

    assert entry == BibEntry(
        entry_type='book',
        entry_name='BerghLofstrom1976InterpolationSpaces',
        title='Interpolation Spaces',
        subtitle='An Introduction',
        publisher='Springer Berlin Heidelberg',
        authors=[
            BibAuthor(full_name='Jöran Bergh'),
            BibAuthor(full_name='Jörgen Löfström')
        ],
        doi=doi,
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
            BibAuthor(full_name='George M. Bergman')
        ],
        doi=doi,
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
        entry_name='BaezStay2010RosettaStone',
        title='Physics, Topology, Logic and Computation',
        subtitle='A Rosetta Stone',
        publisher='Springer Berlin Heidelberg',
        authors=[
            BibAuthor(full_name='J. Baez'),
            BibAuthor(full_name='M. Stay')
        ],
        doi=doi,
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
            BibAuthor(full_name='Nicolas Bourbaki')
        ],
        doi=doi,
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
        entry_name='BoydVandenberghe2019AppliedLinearAlgebra',
        title='Introduction to Applied Linear Algebra',
        subtitle='Vectors, Matrices, and Least Squares',
        publisher='Cambridge University Press & Assessment',
        authors=[
            BibAuthor(full_name='Stephen Boyd'),
            BibAuthor(full_name='Lieven Vandenberghe')
        ],
        doi=doi,
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
        entry_name='IEEEIEEEStandard',
        title='IEEE Standard for Floating-Point Arithmetic',
        publisher='IEEE',
        authors=[
            BibAuthor(full_name='IEEE')
        ],
        doi=doi,
        isbn='978-1-5044-5924-2',
        language='english',
    )
