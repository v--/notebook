import pathlib

from ...common.file_names import escape_file_name


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent


def get_doi_fixture_path(identifier: str) -> pathlib.Path:
    return FIXTURE_DIR / f'{escape_file_name(identifier)}.json'
