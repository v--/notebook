from ..common.network import fetch_html
from .fixtures import get_mathnet_fixture_path


def fetch_mathnet_html(identifier: str, *, dump_as_fixture: bool = False) -> str:
    html = fetch_html(f'https://www.mathnet.ru/rus/{identifier}', 'cp1251')

    if dump_as_fixture:
        with get_mathnet_fixture_path(identifier).open('w') as file:
            file.write(html)

    return html
