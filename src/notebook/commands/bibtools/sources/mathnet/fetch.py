from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ...exceptions import BibToolsNetworkError, BibToolsNotFoundError
from .fixtures import get_mathnet_fixture_path


FIELDS = [
  'authors',
  'description',
  'industryIdentifiers',
  'language',
  'publishedDate',
  'publisher',
  'subtitle',
  'title'
]


def fetch_mathnet_html(identifier: str, *, dump_as_fixture: bool = False) -> str:
    try:
        req = Request(f'https://www.mathnet.ru/rus/{identifier}')
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0')
        res = urlopen(req)
    except HTTPError as err:
        if err.code == 404:
            raise BibToolsNotFoundError(f'Could not find paper with identifier {identifier!r}') from err

        raise BibToolsNetworkError('Error while fetching data') from err

    html = res.read().decode('cp1251')

    if dump_as_fixture:
        with get_mathnet_fixture_path(identifier).open('w') as file:
            file.write(html)

    return html
