import pathlib


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / 'fixtures'


def get_arxiv_fixture_path(identifier: str) -> pathlib.Path:
    return FIXTURE_DIR / f'{identifier.replace('/', '_')}.xml'
