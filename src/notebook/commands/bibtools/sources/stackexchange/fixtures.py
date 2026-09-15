import pathlib


FIXTURE_DIR = pathlib.Path(__file__).resolve().parent / 'fixtures'


def get_stackexchange_fixture_path(site: str, post_id: int, *, is_answer: bool) -> pathlib.Path:
    return FIXTURE_DIR / ('answers' if is_answer else 'questions') / site / f'{post_id}.json'
