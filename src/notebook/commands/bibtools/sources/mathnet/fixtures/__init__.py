import pathlib


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent


def get_mathnet_fixture_path(identifier: str) -> pathlib.Path:
    return FIXTURE_DIR / f'{identifier}.html'
