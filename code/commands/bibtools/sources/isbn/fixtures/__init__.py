import pathlib

from stdnum import isbn


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent


def get_isbn_fixture_path(identifier: str) -> pathlib.Path:
    return FIXTURE_DIR / f'{isbn.format(identifier)}.json'
