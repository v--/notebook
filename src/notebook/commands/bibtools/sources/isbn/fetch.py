from urllib.error import HTTPError
from urllib.request import urlopen

from notebook.commands.bibtools.exceptions import BibToolsNetworkError


def fetch_isbn_json(identifier: str) -> str:
    try:
        res = urlopen(f'https://openlibrary.org/api/books?bibkeys=ISBN:{identifier}&jscmd=details&format=json')
    except HTTPError as err:
        raise BibToolsNetworkError('Error while fetching data') from err

    return res.read().decode('utf-8')
