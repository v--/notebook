from notebook.support.coderefs import collector
from notebook.support.pytest import pytest_parametrize_kwargs

from .distance import hamming, wagner_fisher


@pytest_parametrize_kwargs(
    dict(a='', b='', dist=0),
    *collector.ref_proxy('ex:def:levenshtein_distance/shift',
        dict(a='ac', b='ba', dist=2),
        dict(a='abc', b='bca', dist=3),
        dict(a='abbc', b='bbca', dist=3),
        dict(a='abbbc', b='bbbca', dist=3),
    ),
)
def test_hamming(a: str, b: str, dist: int) -> None:
    assert hamming(a, b) == dist


@pytest_parametrize_kwargs(
    dict(a='', b='', dist=0),
    dict(a='test', b='test', dist=0),
    *collector.ref_proxy('ex:def:levenshtein_distance/shift',
        dict(a='ac', b='ba', dist=2),
        dict(a='abc', b='bca', dist=2),
        dict(a='abbc', b='bbca', dist=2),
        dict(a='abbbc', b='bbbca', dist=2),
    ),
    *collector.ref_proxy('ex:def:levenshtein_distance/spelling',
        dict(a='conunction', b='conjunction', dist=1),
        dict(a='conunction', b='junction', dist=3),
        dict(a='conunction', b='disjunction', dist=4),
        dict(a='subjunction', b='conjunction', dist=3),
        dict(a='subjunction', b='junction', dist=3),
        dict(a='subjunction', b='disjunction', dist=3),
    ),
)
def test_wagner_fisher(a: str, b: str, dist: int) -> None:
    assert wagner_fisher(a, b) == dist
