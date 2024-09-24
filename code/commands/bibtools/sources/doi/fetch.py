from urllib.error import HTTPError
from urllib.request import Request, urlopen

from ...exceptions import BibToolsNetworkError, BibToolsNotFoundError
from .fixtures import get_doi_fixture_path


def fetch_doi_json(identifier: str, *, dump_as_fixture: bool = False) -> str:
    req = Request(
        f'https://dx.doi.org/{identifier}',
        headers={'Accept': 'application/vnd.citationstyles.csl+json'}
    )

    try:
        res = urlopen(req)
    except HTTPError as err:
        if err.code == 404:
            raise BibToolsNotFoundError(f'Could not find object with DOI {identifier}') from err

        raise BibToolsNetworkError('Error while fetching data') from err

    json_body = res.read().decode('utf-8')

    if dump_as_fixture:
        with get_doi_fixture_path(identifier).open('w') as file:
            file.write(json_body)

    return json_body
