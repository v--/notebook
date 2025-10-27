from .distance import hamming, wagner_fisher


def test_hamming() -> None:
    assert hamming('', '') == 0
    assert hamming('test', 'test') == 0

    # ex:def:levenshtein_distance/shift
    assert hamming('ac', 'ba') == 2
    assert hamming('abc', 'bca') == 3
    assert hamming('abbc', 'bbca') == 3
    assert hamming('abbbc', 'bbbca') == 3


def test_wagner_fisher() -> None:
    assert wagner_fisher('', '') == 0
    assert wagner_fisher('test', 'test') == 0

    # ex:def:levenshtein_distance/shift
    assert wagner_fisher('ac', 'ba') == 2
    assert wagner_fisher('abc', 'bca') == 2
    assert wagner_fisher('abbc', 'bbca') == 2
    assert wagner_fisher('abbbc', 'bbbca') == 2
