from .grammar import Grammar
from .chomsky import is_context_free, is_epsilon_free, is_essentially_epsilon_free

from .test_grammar import an


def test_an(an: Grammar):
    assert not is_epsilon_free(an)
    assert is_essentially_epsilon_free(an)
    assert is_context_free(an)
