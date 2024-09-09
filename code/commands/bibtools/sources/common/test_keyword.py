from ..arxiv.model import parse_arxiv_xml
from ..arxiv.paths import get_arxiv_fixture_path
from .keywords import extract_keyphrase


def test_extract_keyphrase_1606_08092v1() -> None:
    with get_arxiv_fixture_path('1606.08092v1').open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    keyphrase = extract_keyphrase(feed.entries[0].title.value, language='en', additional_text=feed.entries[0].summary)
    assert keyphrase == 'Minimal Logic'


def test_extract_keyphrase_2011_00412v3() -> None:
    with get_arxiv_fixture_path('2011.00412v3').open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    keyphrase = extract_keyphrase(feed.entries[0].title.value, language='en', additional_text=feed.entries[0].summary)
    assert keyphrase == 'Lebesgue integration'


def test_extract_keyphrase_1010_0824v13() -> None:
    with get_arxiv_fixture_path('1010.0824v13').open() as file:
        xml_body = file.read()

    feed = parse_arxiv_xml(xml_body)
    keyphrase = extract_keyphrase(feed.entries[0].title.value, language='en', additional_text=feed.entries[0].summary)
    assert keyphrase == 'Mathematical analysis'
