from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

from ...exceptions import BibToolsNetworkError
from .fixtures import get_isbn_fixture_path


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


def fetch_isbn_json(identifier: str, *, dump_as_fixture: bool = False) -> str:
    search_query = urlencode(
        {
            'q': 'isbn:' + identifier,
            'maxResults': 1,
            'fields': f'items/volumeInfo({','.join(FIELDS)}),items/searchInfo(textSnippet)'
        },
        safe='(),/'
    )

    try:
        res = urlopen(
            f'https://www.googleapis.com/books/v1/volumes?{search_query}'
        )
    except HTTPError as err:
        raise BibToolsNetworkError('Error while fetching data') from err

    json_body = res.read().decode('utf-8')

    if dump_as_fixture:
        with get_isbn_fixture_path(identifier).open('w') as file:
            file.write(json_body)

    return json_body
