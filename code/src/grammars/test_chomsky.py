from .grammar import Grammar
from .chomsky import is_context_free, is_epsilon_free, is_essentially_epsilon_free, is_regular
from .fixtures import *


def test_an(an: Grammar):
    assert not is_epsilon_free(an)
    assert is_essentially_epsilon_free(an)
    assert is_context_free(an)
    assert is_regular(an)


def test_anbn(anbn: Grammar):
    assert not is_epsilon_free(anbn)
    assert is_essentially_epsilon_free(anbn)
    assert is_context_free(anbn)
    assert not is_regular(anbn)


def test_s3(s3: Grammar):
    assert not is_epsilon_free(s3)
    assert not is_essentially_epsilon_free(s3)
    assert is_context_free(s3)
    assert not is_regular(s3)
