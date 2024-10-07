from collections.abc import Collection
from textwrap import dedent

import pytest

from .parsing import tokenize_text
from .token_sequence import TokenSequence


@pytest.fixture
def quick_fox() -> TokenSequence:
    return tokenize_text('The quick brown fox jumps over the lazy dog')


@pytest.fixture
def fifth_postulate() -> TokenSequence:
    # Taken verbatim from Fitzgerald's translation of Euclid's elements
    return tokenize_text(
        'And that if a straight-line falling across two (other) straight-lines makes internal angles on the same side (of itself whose sum is) less than two right-angles, then the two (other) straight-lines, being produced to infinity, meet on that side (of the original straight-line) that the (sum of the internal angles) is less than two right-angles (and do not meet on the other side).'
    )


@pytest.fixture
def fifth_postulate_stop_words() -> Collection[str]:
    return 'a across and being do if is itself less makes not of on other same than that the then to two whose'.split()
