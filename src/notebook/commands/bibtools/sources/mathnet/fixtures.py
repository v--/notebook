import pathlib

from notebook.commands.bibtools.sources.helpers.file_names import escape_file_name


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / 'fixtures'


def get_mathnet_fixture_path(identifier: str) -> pathlib.Path:
    return FIXTURE_DIR / f'{escape_file_name(identifier)}.html'
