from urllib.error import HTTPError
from urllib.request import Request, urlopen

from notebook.commands.bibtools.exceptions import BibToolsNetworkError

from .fixtures import get_stackexchange_fixture_path


def fetch_stackexchange_json(site: str, post_id: int, *, is_answer: bool, dump_as_fixture: bool = False) -> str:
    req = Request(f'https://api.stackexchange.com/{'answers' if is_answer else 'questions'}/{post_id}?site={site}')

    try:
        res = urlopen(req)
    except HTTPError as err:
        raise BibToolsNetworkError(f'HTTP error {err.code} while fetching data') from err

    json_body = res.read().decode('utf-8')

    if dump_as_fixture:
        path = get_stackexchange_fixture_path(site, post_id, is_answer=is_answer)
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(json_body)

    return json_body
