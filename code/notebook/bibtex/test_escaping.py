from .escaping import escape


def test_escape_noop() -> None:
    def t(string: str) -> bool:
        return string == escape(string)

    assert t('')
    assert t('test')
    assert t('test test')
    assert t('\\\\')
    assert t('\\&')


def test_escape() -> None:
    assert escape('&') == '\\&'
    assert escape('test & test') == 'test \\& test'
