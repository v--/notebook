from ..common.network import fetch_html
from .fixtures import get_stackexchange_fixture_path


def fetch_stackexchange_html(identifier: str, *, dump_as_fixture: bool = False) -> str:
    html = fetch_html(identifier)

    if dump_as_fixture:
        with get_stackexchange_fixture_path(identifier).open('w') as file:
            file.write(html)

    return html
