from urllib.error import HTTPError
from urllib.request import urlopen

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
        res = urlopen(
            f'https://mi.mathnet.ru/{identifier}'
        )
    except HTTPError as err:
        if err.code == 404:
            raise BibToolsNotFoundError(f'Could not find paper with identifier {identifier!r}') from err

        raise BibToolsNetworkError('Error while fetching data') from err


    html = res.read().decode('cp1251')

    if dump_as_fixture:
        with get_mathnet_fixture_path(identifier).open('w') as file:
            file.write(html)

    return html
