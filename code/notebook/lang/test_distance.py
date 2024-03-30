from .distance import fisher_wagner, hamming


def test_hamming():
    assert hamming('', '') == 0
    assert hamming('test', 'test') == 0

    # ex:def:levenshtein_distance/shift
    assert hamming('ac', 'ba') == 2
    assert hamming('abc', 'bca') == 3
    assert hamming('abbc', 'bbca') == 3
    assert hamming('abbbc', 'bbbca') == 3


def test_fisher_wagner():
    assert fisher_wagner('', '') == 0
    assert fisher_wagner('test', 'test') == 0

    # ex:def:levenshtein_distance/shift
    assert fisher_wagner('ac', 'ba') == 2
    assert fisher_wagner('abc', 'bca') == 2
    assert fisher_wagner('abbc', 'bbca') == 2
    assert fisher_wagner('abbbc', 'bbbca') == 2
