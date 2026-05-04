from .languages import get_language_code, get_language_name


def test_normalize_language() -> None:
    assert get_language_name('english') == 'english'
    assert get_language_name('en') == 'english'

    assert get_language_name('russian') == 'russian'
    assert get_language_name('ru') == 'russian'

    assert get_language_name('czech') == 'czech'
    assert get_language_name('cs') == 'czech'


def test_get_language_code() -> None:
    assert get_language_code('english') == 'en'
    assert get_language_code('en') == 'en'

    assert get_language_code('russian') == 'ru'
    assert get_language_code('ru') == 'ru'

    assert get_language_code('czech') == 'cs'
    assert get_language_code('cs') == 'cs'
