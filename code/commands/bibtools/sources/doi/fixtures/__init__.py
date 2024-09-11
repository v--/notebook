import pathlib


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent


def get_doi_fixture_path(doi: str) -> pathlib.Path:
    return FIXTURE_DIR / f'{doi.replace('/', '_')}.json'

