import pathlib


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent


def get_arxiv_fixture_path(arxiv_id: str) -> pathlib.Path:
    return FIXTURE_DIR / f'{arxiv_id.replace('/', '_')}.xml'
