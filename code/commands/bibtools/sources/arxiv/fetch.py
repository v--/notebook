from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from ...exceptions import BibToolsNetworkError
from .paths import get_arxiv_fixture_path


def fetch_arxiv_xml(identifier: str, *, dump_as_fixture: bool = False) -> str:
    search_query = urlencode({
        'max_results': 1,
        'id_list': identifier,
        'sortBy': 'submittedDate'
    })

    try:
        res = urlopen(
            f'https://export.arxiv.org/api/query?{search_query}'
        )
    except HTTPError as err:
        raise BibToolsNetworkError('Error while fetching data') from err

    xml_body = res.read().decode('utf-8')

    if dump_as_fixture:
        with get_arxiv_fixture_path(identifier).open('w') as file:
            file.write(xml_body)

    return xml_body
