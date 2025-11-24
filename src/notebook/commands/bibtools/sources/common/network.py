from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ...exceptions import BibToolsNetworkError


def fetch_html(url: str, encoding: str = 'utf-8') -> str:
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0')
        res = urlopen(req)
    except HTTPError as err:
        raise BibToolsNetworkError(f'HTTP error {err.code} while fetching data') from err

    return res.read().decode(encoding)
